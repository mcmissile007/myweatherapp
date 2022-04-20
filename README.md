# myweatherapp
Application to get the current weather and weather forecast for a given location \
@Arguments\
    Positionals and required:\
        command : current or forecast \
        locations: in "{city},{country code}" format. \
    Optionals:\
        --units (metric or imperial)\
        --days (integer between 1 and 5)\


Examples:\
myweatherapp current Irvine,US --units=imperial\
myweatherapp forecast Santander,ES --days=3

