import re
from typing import Union

from fastnumbers import fast_real


def map_value(value: str) -> Union[str, int, float]:
    # Handle fractions
    if '/' in value:
        match = re.match(r'^(?:(\d+)[ -])?(\d+)/(\d+) ?$', value)
        if match:
            whole, numerator, denominator = match.groups()
            return int(whole or '0') + int(numerator) / int(denominator)
        else:
            raise f"Failed to match fraction '{value}'"

    value = value.replace(',', '').replace(' ', '')
    if re.match(r'^-?(\d+(\.\d+)?|(\.\d+))$', value):
        return fast_real(value)

    return value


def map_units(unit: str) -> str:
    if re.match(r'^btu$', unit, re.IGNORECASE):
        return 'BTU'
    if re.match(r'^btuh( cooling| heat)?$', unit, re.IGNORECASE):
        return 'BTUH'
    if re.match(r'^cfm$', unit, re.IGNORECASE):
        return 'cfm'
    if re.match(r"^'$", unit):
        return 'ft'
    if re.match(r'^gal(lon)?$', unit, re.IGNORECASE):
        return 'gal'
    if re.match(r'^gph$', unit, re.IGNORECASE):
        return 'gph'
    if re.match(r'^gpm$', unit, re.IGNORECASE):
        return 'gpm'
    if re.match(r'^h\.?p\.?$', unit, re.IGNORECASE):
        return 'hp'
    if re.match(r'^"$', unit):
        return 'in'
    if re.match(r'^kva$', unit, re.IGNORECASE):
        return 'kVA'
    if re.match(r'^kw$', unit, re.IGNORECASE):
        return 'kW'
    if re.match(r'^lb\.?$', unit, re.IGNORECASE):
        return 'lb'
    if re.match(r'^lb\.?(/| per )h(ou)?r\.?$', unit, re.IGNORECASE):
        return 'lb/h'
    if re.match(r'^mbh$', unit, re.IGNORECASE):
        return 'MBH'
    if re.match(r'^mbh input$', unit, re.IGNORECASE):
        return 'MBH input'
    if re.match(r'^psig$', unit, re.IGNORECASE):
        return 'psig'
    if re.match(r'^to?n$', unit, re.IGNORECASE):
        return 'ton'
    if re.match(r'^volt$', unit, re.IGNORECASE):
        return 'V'
    if re.match(r'^w$', unit, re.IGNORECASE):
        return 'W'
    raise f"Failed to match unit '{unit}'"


value_re = '(to )?([0-9,-.<>/ ]+)'
units_re = '([a-zA-Z./"\' ]+)'

cols_with_units = ['POWER', 'FLOWRATE', 'CAPACITY', 'SIZE', 'LOA', 'VOLTAGE', 'LENGTH']


def disaggregate_units(record):
    for col in cols_with_units:
        if col in record:
            full_value = record[col].replace(' to ', '-')

            # Check for values with units
            match = re.match(f"^{value_re} ?{units_re}$", full_value)
            if match:
                to_value, value, units = match.groups()
                record[col] = map_value(f"<{value}") if to_value else map_value(value)
                record[f"{col}_UNITS"] = map_units(units)
                continue

            # Check for missing units
            match = re.match(f"^{value_re}$", full_value)
            if match:
                to_value, value = match.groups()

                # Handle known missing units
                if record['FUEL_TYPE'] == 'Gas/Oil' and record['TYPE'] == 'Fire Tube' and record['CAPACITY'] in ['5,000-7,500', '7,500-12,500', '12,500-20,000']:
                    record[col] = map_value(value)
                    record[f"{col}_UNITS"] = 'MBH'
                    continue

                # Unknown missing units
                record[col] = map_value(f"<{value}") if to_value else map_value(value)
                record[f"{col}_UNITS"] = 'UNKNOWN'
                continue

            # Check for doubles
            match = re.match(f"^{value_re} ?{units_re}, {value_re} ?{units_re}$", full_value)
            if match:
                to_value_a, value_a, units_a, to_value_b, value_b, units_b = match.groups()
                del record[col]
                record[f"{col}_COOLING"] = map_value(f"<{value_a}") if to_value_a else map_value(value_a)
                record[f"{col}_COOLING_UNITS"] = map_units(units_a)
                record[f"{col}_HEATING"] = map_value(f"<{value_b}") if to_value_b else map_value(value_b)
                record[f"{col}_HEATING_UNITS"] = map_units(units_b)
                continue
            print(f"Failed to match '{full_value}'")

    # Sort properties
    return dict(sorted(record.items()))


def disaggregate_capacity(record, uniformat):
    # HEAT GENERATING SYSTEMS
    if uniformat == 'D3020' and record.get('CAPACITY_UNITS') in ['BTU', 'MBH']:
        record['CAPACITY_HEATING'] = record.pop('CAPACITY')
        record['CAPACITY_HEATING_UNITS'] = record.pop('CAPACITY_UNITS')
    # COOLING GENERATING SYSTEMS
    elif uniformat == 'D3030' and record.get('CAPACITY_UNITS') == 'ton' and record.get('EQUIPMENT') != 'Cooling Tower':
        record['CAPACITY_COOLING'] = record.pop('CAPACITY')
        record['CAPACITY_COOLING_UNITS'] = record.pop('CAPACITY_UNITS')
    # TERMINAL & PACKAGE UNITS
    elif uniformat == 'D3050':
        if record.get('CAPACITY_UNITS') == 'ton':
            record['CAPACITY_COOLING'] = record.pop('CAPACITY')
            record['CAPACITY_COOLING_UNITS'] = record.pop('CAPACITY_UNITS')
        elif record.get('CAPACITY_UNITS') in ['BTU', 'MBH']:
            record['CAPACITY_HEATING'] = record.pop('CAPACITY')
            record['CAPACITY_HEATING_UNITS'] = record.pop('CAPACITY_UNITS')

    return record
