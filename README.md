
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


## Visilization Setting 
* step1: Type $your IP:3000
* step2: Go to Plugins and install Business Media 
* step3: Import ./EII Video and Time Series Dashboard.json 
* step4: Result
<img src="figs/operation.gif" width="550" height="300"/>



