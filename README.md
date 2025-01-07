# NCS in EII System Container Setup

## Overview

This guide will walk you through the process of setting up and running the NCS in the EII (Edge Insights for Industrial) system container.

---

## Prerequisites

- Ensure the `ai_toolwear_ncs/` folder is placed at the same path level as the `IEdgeInsights/` folder. For example:

    ```bash
    /home/edge_insights_industrial/Edge_Insights_for_Industrial_4.1.0/IEdgeInsights
    ```

---

## Build NCS in EII System Container

1. Navigate to the `IEdgeInsights` directory:

    ```bash
    cd /home/edge_insights_industrial/Edge_Insights_for_Industrial_4.1.0/IEdgeInsights
    ```

2. Run the following commands to set up the container and build the procedure:

    ```bash
    sh ../ai_toolwear_ncs/run_container.sh
    sh ./build/build_procedure.sh
    ```

3. You will now be inside the container at the following path:

    ```bash
    root@ai_toolwear_ncs:/app
    ```

---

## Run ToolWear Program

1. **Check NCS Name**  
   To verify the NCS device name, run the following command:

    ```bash
    python3 check_device.py
    ```

2. **Inference**  
   Navigate to the `code` directory and execute the inference script:

    ```bash
    cd code
    sh run.sh
    ```

---

## Visualization Setup

1. **Step 1: Access the Dashboard**  
   Open a web browser and navigate to your IP address at port `3000`:

    ```bash
    http://$your_IP:3000
    ```

2. **Step 2: Install the Plugin**  
   Go to the **Plugins** section and install **Business Media**.

3. **Step 3: Import the Dashboard**  
   Import the following JSON dashboard:

    ```bash
    ./EII_Video_and_TimeSeries_Dashboard.json
    ```

4. **Step 4: View Results**  
   After importing the dashboard, you will see the results visualized in the dashboard. Example:

   ![Result GIF](dashboard.gif)
   
