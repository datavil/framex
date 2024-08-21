import frames as fx

print(fx.available(option="remote")) # remote only
print(fx.available(option="local")) # locally cached
print(fx.available(option=None)) # all available
