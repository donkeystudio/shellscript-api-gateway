# Shell Script API Gateway
An application to trigger shell scripts via a REST API. Endpoints and target scripts are configurable via a config file. API Key authentication is supported.

## [Docker](https://hub.docker.com/r/donkeystudio/shellscript-api-gateway)
Supported architectures: `linux/arm/v7`, `linux/arm64`, `linux/amd64`

## Dependencies
```bash
python3 -m pip install -r requirements.txt
```

## Startup Configuration
```bash
python3 main.py --help
```

```bash
usage: main.py [-h] [-conf CONFIG_FILE] [-p PORT] [-log LOG_FILE] [-d DEBUG_LEVEL]

optional arguments:
  -h,                           --help                                  show this help message and exit
  -conf     CONFIG_FILE,        --config_file       CONFIG_FILE         Location of the application config file (default: ./config.properties)
  -p        PORT,               --port              PORT                Port (default: 8080)
  -log      LOG_FILE,           --log_file          LOG_FILE            Location of the log file. Default is system log
  -logsize  LOG_MAX_SIZE,       --log_max_size      LOG_MAX_SIZE        Max file size in MB before it is rotated. Set 0 to turn off log rotation (default: 1)
  -logcount LOG_BACKUP_COUNT,   --log_backup_count  LOG_BACKUP_COUNT    Max number of rotated backup log file. (default: 5)
  -d        DEBUG_LEVEL,        --debug_level       DEBUG_LEVEL         Debug Level CRITICAL/ERROR/WARNING/INFO/DEBUG. Default is WARNING (default: WARNING)
```

### Config file
The main config file consists of 2 sections:
```json
[SHELL_GATEWAY]
END_POINTS= [
            {
                "uri": <Endpoint URI>,
                "api_key":
                {
                    "key": <Required. API Key of the service. In Base64 encoded format. Leave empty string if API Key is disabled.>,
                    "header": <Required. Header field where the API Key is stored. Leave empty string if API Key is disabled.>
                },
                "target": <Target script>
            },
            {
                ....
            }
        ]

[REQUEST_SCHEMA]
SCHEMA={
        "type" : "object",
        "properties" :
        {
            "args":
            {
                "type" : "array"
            }
        },
        "required":
        [
            "args"
        ]
    }
```

## API End-points
API End-points are defined under [SHELL_GATEWAY] -> END_POINTS. API Key authentication is supported.

### General response example
Success
```json
{
    "status": 200,
    "data": "1 2 test\n"
}
```
Failed
```json
{
    "status": 400,
    "message": "Invalid request data"
}
```

### Request body
All requests must include the following json body
```json
{
    "args":[<All script arguments>]
}
```
