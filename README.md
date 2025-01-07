
## Build NCS in EII System Container
Put the ai_toolwear_ncs/ with same path level with  IEdgeInsights/
```bash
cd /home/edge_insights_industrial/Edge_Insights_for_Industrial_4.1.0/IEdgeInsights
sh ../ai_toolwear_ncs/run_container.sh 
sh ./build/build_procedure.sh
````

You will access into container and at the following path
root@ai_toolwear_ncs:/app

## Run ToolWear program
* Check NCS name
 ```bash
python3 check_device.py
````
 
* Inference
```bash
cd code
sh run.sh 
````

## Visilization with Grafana
Type $your IP:3000
 ```bash
python3 check_device.py
````

* Result
<img src="figs/operation.gif" width="550" height="300"/>



