Usage with NAGIOS

Define a command check in **commands.cfg**

```bash
define command
 {
        command_name check_p81_network_health
        command_line /usr/local/nagios/libexec/check_health_p81_wrapper.sh
 }
```
  
Define a command check in **localhost.cfg**

```bash
define service {

    use                     local-service           ; Name of service template to use
    host_name               localhost
    service_description     P81 GW HEALTH
    check_command           check_p81_network_health
    notifications_enabled   0
    max_check_attempts              3
    normal_check_interval           0.1
    retry_check_interval            0.1
    notification_interval           60
}
```

Pre-flight check
```
/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
```

Restart NAGIOS - service nagios restart


Slack Messaging Webhook

```
    json_header = {}
    json_header['Content-Type'] = 'application/json'
    data={}
    data['text'] = str(','.join(monitoring_results))
    data['icon_url'] = 'https://img.icons8.com/emoji/96/000000/penguin--v2.png'
    data['username'] = 'Perimeter81 API'

    payload = json.dumps(data);
    #print(payload)
    #print(slack_data)
    slack_call = requests.post(slack_url, headers=json_header, data=payload)

    print(slack_call.text)
    print(slack_call.content)
    print(slack_call.status_code)
    ```
