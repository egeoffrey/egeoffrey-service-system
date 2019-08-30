### service/system: collect telemetry information from the system
## HOW IT WORKS: 
## DEPENDENCIES:
# OS: 
# Python: 
## CONFIGURATION:
# required: 
# optional: 
## COMMUNICATION:
# INBOUND: 
# - IN: 
#   required: measure
#   optional: 
# OUTBOUND: 

from sdk.python.module.service import Service

import sdk.python.utils.command

class System(Service):
    # What to do when initializing
    def on_init(self):
        # define common commands
        self.commands = {
            'cpu_user': 'top -bn1 | grep "Cpu(s)"|awk \'{print $2}\'',
            'cpu_system': 'top -bn1 | grep "Cpu(s)"|awk \'{print $4}\'',
            'ram_used': 'free -m | grep Mem:|awk \'{print $3}\'',
            'swap_used': 'free -m | grep Swap:|awk \'{print $3}\'',
            'load_1': 'uptime | awk \'{gsub(",","",$(NF-2)); print $(NF-2)}\'',
            'load_5': 'uptime | awk \'{gsub(",","",$(NF-1)); print $(NF-1)}\'',
            'load_15': 'uptime | awk \'{gsub(",","",$(NF-0)); print $(NF-0)}\'',
            'network_services': 'netstat -tunap 2>/dev/null | grep tcp|grep LISTEN|wc -l',
            'network_connections': 'netstat -tunap 2>/dev/null |grep tcp|grep -v LISTEN|wc -l',
            'temperature': 'cat /sys/class/thermal/thermal_zone0/temp | awk \'{printf "%.1f",$0/1000}\'',
            'uptime': 'cat /proc/uptime | cut -f 1 -d "."',
            'logwatch': 'logwatch --range yesterday --output stdout --format text | cat',
            'reboot': 'reboot',
            'shutdown': 'shutdown -h now',
            'system_logs': 'tail -100 /var/log/messages | perl -ne \'/^(\\S+ \\S+ \\S+) \\S+ (\\S+): (.+)$/;print \"$1|_|$2|_|$3\\n\"\'',
        }
    
    # What to do when running
    def on_start(self):
        pass
    
    # What to do when shutting down    
    def on_stop(self):
        pass

    # What to do when receiving a request for this module        
    def on_message(self, message):
        if message.command == "IN":
            sensor_id = message.args
            # ensure configuration is valid
            if not self.is_valid_configuration(["measure"], message.get_data()): return
            measure = message.get("measure")
            if measure not in self.commands:
                self.log_error("invalid measure "+measure)
                return                
            # run the command
            data = sdk.python.utils.command.run(self.commands[measure])
            # send the response back
            message.reply()
            message.set("value", data)
            self.send(message)
            
    # What to do when receiving a new/updated configuration for this module
    def on_configuration(self,message):
        # register/unregister the sensor
        if message.args.startswith("sensors/"):
            if message.is_null: 
                sensor_id = self.unregister_sensor(message)
            else: 
                sensor_id = self.register_sensor(message)
