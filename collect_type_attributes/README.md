# Collect type attributes
Use wsadmin for collect base type attributes. The attributes collected and stored to ./out directory

### Example output
```json
[
  {
    "name": "numberOfUnsharedPoolPartitions",
    "type": "int",
    "list": false,
    "reference": false,
    "required": false,
    "base": false,
    "default-value": "0",
    "variants": "",
    "position": 9
  },
  {
    "name": "properties",
    "type": "Property",
    "list": true,
    "reference": false,
    "required": false,
    "base": true,
    "default-value": "",
    "variants": "DiscoverableDescriptiveProperty,TypedProperty,DescriptiveProperty",
    "position": 19
  },
  {
    "name": "purgePolicy",
    "type": "ENUM",
    "list": false,
    "reference": false,
    "required": false,
    "base": false,
    "default-value": "FailingConnectionOnly",
    "variants": "EntirePool,FailingConnectionOnly",
    "position": 7
  }
]
```