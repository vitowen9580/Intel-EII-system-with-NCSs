

try:
    from openvino.inference_engine import IENetwork, ExecutableNetwork, IECore
    import openvino.inference_engine.ie_api
except:
    print(RED + '\nPlease make sure your OpenVINO environment variables are set by sourcing the' + YELLOW + ' setupvars.sh ' + RED + 'script found in <your OpenVINO install location>/bin/ folder.\n' + NOCOLOR)
    exit(1)




ie = IECore()
for device_name in ie.available_devices:
    if(device_name.find('MYRIAD')>-1):
          print(device_name)
