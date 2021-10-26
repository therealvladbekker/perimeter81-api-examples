<code>
  define command{
        command_name check_p81_network_health
        command_line /usr/local/nagios/libexec/check_health_p81_wrapper.sh
        #command_line /usr/local/nagios/libexec/check_health.py -H $ARG1$ -c $ARG2$ -d $ARG3$
}
<code>
