<<<<<<< HEAD
# Intel-EII-system-with-NCSs
=======
# Contents

- [Contents](#contents)
  - [About Edge Insights for Industrial](#about-edge-insights-for-industrial)
  - [Minimum System Requirements](#minimum-system-requirements)
  - [Install Edge Insights for Industrial from source code](#install-Edge-insights-for-industrial-from-source-code)
    - [Manual Installation](#manual-installation)
      - [Task 1: Install Prerequisites](#task-1-install-prerequisites)
        - [Run the Prerequisites Script](#run-the-prerequisites-script)
        - [Optional Steps](#optional-steps)
          - [Method 1](#method-1)
          - [Method 2](#method-2)
      - [Task 2: Generate the Deployment and the Configuration Files](#task-2-generate-the-deployment-and-the-configuration-files)
        - [Use the Builder Script](#use-the-builder-script)
        - [Generate Consolidated Files for All Applicable Services of Edge Insights for Industrial](#generate-consolidated-files-for-all-applicable-services-of-Edge-insights-for-industrial)
        - [Generate Consolidated Files for a Subset of Edge Insights for Industrial Services](#generate-consolidated-files-for-a-subset-of-Edge-insights-for-industrial-services)
        - [Generate Multi-instance Config Using the Builder](#generate-multi-instance-config-using-the-builder)
        - [Generate Benchmarking Config Using Builder](#generate-benchmarking-config-using-builder)
      - [Task 3: Build and Run the Edge Insights for Industrial Video and Time Series Use Cases](#task-3-build-and-run-the-Edge-insights-for-industrial-video-and-time-series-use-cases)
        - [Independent building and deployment of services](#independent-building-and-deployment-of-services)
        - [Build the Edge Insights for Industrial Stack](#build-the-Edge-insights-for-industrial-stack)
        - [Run Edge Insights for Industrial Services](#run-Edge-insights-for-industrial-services)
          - [Provision Edge Insights for Industrial](#provision-Edge-insights-for-industrial)
          - [Start Edge Insights for Industrial in Dev Mode](#start-Edge-insights-for-industrial-in-dev-mode)
          - [Start Edge Insights for Industrial in Profiling Mode](#start-Edge-insights-for-industrial-in-profiling-mode)
          - [Run Provisioning Service and Rest of the Edge Insights for Industrial Stack Services](#run-provisioning-service-and-rest-of-the-Edge-insights-for-industrial-stack-services)
  - [Push the Required Edge Insights for Industrial Images to Docker Registry](#push-the-required-Edge-insights-for-industrial-images-to-docker-registry)
  - [List of EII services](#list-of-eii-services)
  - [Adding New Services to EII Stack](#adding-new-services-to-eii-stack)
  - [Video Pipeline Analytics](#video-pipeline-analytics)
      - [Enable Camera-based Ingestion](#enable-camera-based-ingestion)
      - [Integrate Python UDF](#integrate-python-udf)
      - [Use Video Accelerators in Edge Video Analytics Microservice](#use-video-accelerators-in-edge-video-analytics-microservice)
  - [Time Series Analytics](#time-series-analytics)
  - [Edge Insights for Industrial Multi-node Cluster Deployment](#Edge-insights-for-industrial-multi-node-cluster-deployment)
    - [With K8s Orchestrator](#with-k8s-orchestrator)
  - [Edge Insights for Industrial Tools](#Edge-insights-for-industrial-tools)
  - [Edge Insights for Industrial Uninstaller](#Edge-insights-for-industrial-uninstaller)
  - [Debugging Options](#debugging-options)
  - [Web Deployment Tool](#web-deployment-tool)
  - [Troubleshooting Guide](#troubleshooting-guide)

## About Edge Insights for Industrial

Edge Insights for Industrial (EII) is a set of pre-validated ingredients for integrating video and time series data analytics on edge compute nodes. EII includes modules to enable data collection, storage, and analytics for both time series and video data.

> **Note:**
> In this document, you will find labels of `Edge Insights for Industrial (EII)` for file names, paths, code snippets, and so on.

## Minimum System Requirements

The following are the minimum system requirements to run EII:

|System Requirement       |  Details     |
|---    |---    |
|Processor       | 8th generation Intel® CoreTM processor onwards with Intel® HD Graphics or Intel® Xeon® processor |
|RAM       | Minimum 16 GB       |
|Hard drive       | Minimum 128 GB and Recommended 256 GB      |
|Operating system       | Ubuntu 20.04      |

> **Note:**
>
> - To use EII, ensure that you are connected to the internet.
> - The recommended RAM capacity for the Video Analytics pipeline is 16 GB. The recommended RAM for the Time Series Analytics pipeline is 4 GB with Intel® Atom processors.
> - EII is validated on Ubuntu 20.04. You can install EII stack on other Linux distributions with support for docker-ce and docker-compose tools.

## Install Edge Insights for Industrial from source code

By default, EII is installed via Edge Software Hub after downloading the EII package and running command `./edgesoftware install`. This is the recommended installation when you want to preview EII stack.
If you are more interested in knowing different EII configurations that could be exercised or wish to customize the EII source code, please check the below sections:

- [Manual Installation](#manual-installation)
  - [Task 1: Install Prerequisites](#task-1-install-prerequisites)
  - [Task 2: Generate the Deployment and the Configuration Files](#task-2-generate-the-deployment-and-the-configuration-files)
  - [Task 3: Build and Run the EII Video and Time Series Use Cases](#task-3-build-and-run-the-Edge-insights-for-industrial-video-and-time-series-use-cases)

### Manual Installation

Complete the following tasks to install EII manually.

#### Task 1: Install Prerequisites

The `pre_requisites.sh` script automates the installation and configuration of all the prerequisites required for building and running the EII stack. The prerequisites are as follows:

- docker daemon
- docker client
- docker-compose
- Python packages

The `pre-requisites.sh` script performs the following:

- Checks if docker and docker-compose is installed in the system. If required, it uninstalls the older version and installs the correct version of docker and docker-compose.
- Configures the proxy settings for the docker client and docker daemon to connect to the internet.
- Configures the proxy settings system-wide (/etc/environment) and for docker. If a system is running behind a proxy, then the script prompts users to enter the proxy address to configure the proxy settings.
- Configures proxy setting for /etc/apt/apt.conf to enable apt updates and installations.

> **Note:**
>
> - The recommended version of docker is `20.10.6`.
> - The recommended version of the docker-compose is `1.29.0`. In versions older than 1.29.0, the video use case docker-compose.yml files and the device_cgroup_rules command may not work.
> - To use versions older than docker-compose 1.29.0, in the `ia_edge_video_analytics_microservice` service, comment out the `device_cgroup_rules` command.
> - You can comment out the `device_cgroup_rules` command in the `ia_edge_video_analytics_microservice` service to use versions older than 1.29.0 of docker-compose. This can result in limited inference and device support. The following code sample shows how the `device_cgroup_rules` commands are commented out:
>
>  ```sh
>    ia_edge_video_analytics_microservice:
>     ...
>      #device_cgroup_rules:
>         #- 'c 189:* rmw'
>         #- 'c 209:* rmw'
>  ```
>
> After modifying the `docker-compose.yml` file, refer to the `Using the Builder script` section. Before running the services using the `docker-compose up` command, rerun the `builder.py` script.

##### Run the Prerequisites Script

To run the prerequisite script, execute the following commands:

  ```sh
    cd [WORKDIR]/IEdgeInsights/build
    sudo -E ./pre_requisites.sh --help
      Usage :: sudo -E ./pre_requisites.sh [OPTION...]
      List of available options...
      --proxy         proxies, required when the gateway/edge node running EII (or any of EII profile) is connected behind proxy
      --help / -h         display this help and exit
  ```

> **Note:**
>
> If the --proxy option is not provided, then script will run without proxy. Different use cases are as follows:
>
> - Runs without proxy
>
>     ```sh
>      sudo -E ./pre_requisites.sh
>     ```
>
> - Runs with proxy
>
>     ```sh
>     sudo -E ./pre_requisites.sh --proxy="proxy.intel.com:891"
>     ```

##### Optional Steps

- If required, you can enable full security for production deployments. Ensure that the host machine and docker daemon are configured per the security recommendation. For more info, see [build/docker_security_recommendation.md](build/docker_security_recommendation.md).
- If required, you can enable log rotation for docker containers using any of the following methods:

###### Method 1

Set the logging driver as part of the docker daemon. This applies to all the docker containers by default.

1. Configure the json-file driver as the default logging driver. For more info, see [JSON File logging driver](https://docs.docker.com/config/containers/logging/json-file/). The sample json-driver configuration that can be copied to `/etc/docker/daemon.json` is as follows:

    ```json
            {
              "log-driver": "json-file",
              "log-opts": {
              "max-size": "10m",
              "max-file": "5"
              }
          }
    ```

2. Run the following command to reload the docker daemon:

    ```sh
    sudo systemctl daemon-reload
    ```

3. Run the following command to restart docker:

    ```sh
    sudo systemctl restart docker
    ```

###### Method 2

Set logging driver as part of docker compose which is container specific. This overwrites the first option (i.e /etc/docker/daemon.json). The following example shows how to enable the logging driver only for the video_ingestion service:

  ```json
    ia_edge_video_analytics_microservice:
      ...
      ...
      logging:
        driver: json-file
        options:
        max-size: 10m
  max-file: 5
  ```

#### Task 2: Generate the Deployment and the Configuration Files

After downloading EII from the release package or git, run the commands mentioned in this section from the `[WORKDIR]/IEdgeInsights/build/` directory.

##### Use the Builder Script

> **Note**:
> To run the `builder.py` script, complete the prerequisite by entering the values for the following keys in build/.env:
> * ETCDROOT_PASSWORD – The value for this key is required, if you are using the ConfigMgrAgent service.
> * INFLUXDB_USERNAME, INFLUXDB_PASSWORD, MINIO_ACCESS_KEY, and MINIO_SECRET_KEY – The values for these keys are required, if you are using the Data Store service. Special characters `~:'+[/@^{%(-"*|,&<`}._=}!>;?#$)\` are not allowed for the INFLUXDB_USERNAME and INFLUXDB_PASSWORD. The MINIO_ACCESS_KEY and the MINIO_SECRET_KEY length must be a minimum of 8 characters.
> If you enter wrong values or do not enter the values for the keys, the `builder.py` script prompts for corrections or values.
> * PKG_SRC - The value will be pre-populated with the local http server daemon which is brought up by the `./edgesoftware install` command when installed from Edge Software Hub. By default, the EII core libs and other artifacts would be picked up from `$HOME/edge_insights_industrial/Edge_Insights_for_Industrial_<version>/CoreLibs` directory.

To use the `builder.py` script, run the following command:

```sh
    python3 builder.py -h
    usage: builder.py [-h] [-f YML_FILE] [-v VIDEO_PIPELINE_INSTANCES]
                        [-d OVERRIDE_DIRECTORY] [-s STANDALONE_MODE] [-r REMOTE_DEPLOYMENT_MODE]
    optional arguments:
        -h, --help            show this help message and exit
        -f YML_FILE, --yml_file YML_FILE
                            Optional config file for list of services to include.
                            Eg: python3 builder.py -f video-streaming.yml (default: None)
        -v VIDEO_PIPELINE_INSTANCES, --video_pipeline_instances VIDEO_PIPELINE_INSTANCES
                            Optional number of video pipeline instances to be
                            created.
                            Eg: python3 builder.py -v 6 (default: 1)
        -d OVERRIDE_DIRECTORY, --override_directory OVERRIDE_DIRECTORY
                            Optional directory consisting of benchmarking
                            configs to be present in each app directory.
                            Eg: python3 builder.py -d benchmarking (default: None)
        -s STANDALONE_MODE, --standalone_mode STANDALONE_MODE
                            Standalone mode brings in changes to support independently
                            deployable services.
                            Eg: python3 builder.py -s True (default: False)
        -r REMOTE_DEPLOYMENT_MODE, --remote_deployment_mode REMOTE_DEPLOYMENT_MODE
                            Remote deployment mode brings in changes to support remote deployment
                            wherein builder does not auto-populate absolute paths of build 
                            related variables in the generated docker-compose.yml
                            Eg: python3 builder.py -r True (default: False)
```

##### Generate Consolidated Files for All Applicable Services of Edge Insights for Industrial

Using the Builder tool, EII auto-generates the configuration files that are required for deploying the EII services on a single node or multiple nodes. The Builder tool auto-generates the consolidated files by getting the relevant files from the EII service directories that are required for different EII use-cases. The Builder tool parses the top-level directories excluding **EdgeVideoAnalyticsMicroservice** under the `IEdgeInsights` directory to generate the consolidated files.

The following table shows the list of consolidated files and their details:

Table: Consolidated files

| File Name                    | Description                                                                                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| docker-compose.yml           | Consolidated `docker-compose.yml` file used to launch the EII docker containers in each single node using the `docker-compose` tool.                                           |
| docker-compose.override.yml  | Consolidated `docker-compose-dev.override.yml` of every app that is generated only in the DEV mode for the EII deployment on a given single node using the `docker-compose` tool.      |
| eii_config.json              | Consolidated `config.json` of every app that will be put into etcd during provisioning.                                                                                        |
| values.yaml                  | Consolidated `values.yaml` of every app inside the helm-eii/eii-deploy directory that is required to deploy the EII services via helm.                                           |
| Template yaml files          | Files copied from the helm/templates directory of every app to the helm-eii/eii-deploy/templates directory that is required to deploy EII services via helm.                    |

> **Note:**
>
> - If you modify an individual EII app or service directory file, then ensure to rerun the `builder.py` script before running the EII stack to regenerate the updated consolidated files.
> - Manual editing of consolidated files is not recommended. Instead modify the respective files in the EII app or service directories and use the `builder.py` script to generate the consolidated files.
> - Enter the secret credentials in the `# Service credentials` section of the [.env](build/.env) file if you are trying to run that EII app/service. If the required credentials are not present, the `builder.py` script would be prompting until all the required credentials are entered. Apply a file access mask to protect the [.env](build/.env) file from being read by unauthorized users.
> - The [builder_config.json](./build/builder_config.json) is the config file for the `builder.py` script and it contains the following keys:
>   - `subscriber_list`: This key contains a list of services that act as a subscriber to the stream being published.
>   - `publisher_list`: This key contains a list of services that publishes a stream of data.
>   - `include_services`: This key contains the mandatory list of services. These services should be included when the Builder is run without the `-f` flag.
>   - `exclude_services`: This key contains the mandatory list of services. These services should be excluded when the Builder is run without the `-f` flag.
>   - `increment_rtsp_port`: This is a Boolean key. It increments the port number for the RTSP stream pipelines.

To generate the consolidated files, run the following command:

  ```sh
  python3 builder.py
  ```

##### Generate Consolidated Files for a Subset of Edge Insights for Industrial Services

Builder uses a yml file for configuration. The config yml file consists of a list of services to include. You can mention the service name as the path relative to `IEdgeInsights` or full path to the service in the config yml file.
To include only a certain number of services in the EII stack, you can add the -f or yml_file flag of builder.py. You can find the examples of yml files for different use cases as follows:

- [Azure](build/usecases/video-streaming-azure.yml)

  The following example shows running Builder with the -f flag:

    ```sh
       python3 builder.py -f usecases/video-streaming.yml
    ```

- **Main Use Cases**

| Use case                    | yaml file                                                                 |
| -------------------------- |---------------------------------------------------------------------------|
| Video + Time Series         | [build/usecases/video-timeseries.yml](build/usecases/video-timeseries.yml)|
| Video                      | [build/usecases/video.yml](build/usecases/video.yml)                      |
| Time Series                 | [build/usecases/time-series.yml](build/usecases/time-series.yml)          |

- **Video Pipeline Sub Use Cases**

| Use case                                | yaml file                                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| Video streaming with EVAM              | [build/usecases/video-streaming-evam.yml](build/usecases/video-streaming-evam.yml)                      |
| Video streaming and historical         | [build/usecases/video-streaming-evam-datastore.yml](build/usecases/video-streaming-evam-datastore.yml)  |
| Video streaming with AzureBridge       | [build/usecases/video-streaming-azure.yml](build/usecases/video-streaming-azure.yml)                    |

When you run the multi-instance config, a `build/multi_instance` directory is created in the build directory. Based on the number of `video_pipeline_instances` specified, that many directories of EdgeVideoAnalyticsMicroservice are created in the `build/multi_instance` directory.

The following section provides an example for running the Builder to generate the multi-instance boiler plate config for 3 streams of **video-streaming** use case.

##### Generate Multi-instance Config Using the Builder

If required, you can generate the multi-instance `docker-compose.yml` and `config.json` files using the Builder. You can use the `-v` or `video_pipeline_instances` flag of the Builder to generate boiler plate config for the multiple-stream use cases. The `-v` or `video_pipeline_instances` flag creates the multi-stream boiler plate config for the `docker-compose.yml` and `eii_config.json` files.

The following example shows running builder to generate the multi-instance boiler plate config for 3 streams of video-streaming use case:

  ```sh
    python3 builder.py -v 3 -f usecases/video-streaming-evam.yml
  ```

Using the previous command for 3 instances, the `build/multi_instance` directory consists of the following directories

- EdgeVideoAnalyticsMicroservice1
- EdgeVideoAnalyticsMicroservice2
- EdgeVideoAnalyticsMicroservice3

Initially each directory will have the default `config.json` and the `docker-compose.yml` files that are present within the `EdgeVideoAnalyticsMicroservice/eii` directory.

  ```example
    ./build/multi_instance/
    |-- EdgeVideoAnalyticsMicroservice1
    |   |-- config.json
    |   `-- docker-compose.yml
    |-- EdgeVideoAnalyticsMicroservice2
    |   |-- config.json
    |   `-- docker-compose.yml
    |-- EdgeVideoAnalyticsMicroservice3
    |   |-- config.json
    |   `-- docker-compose.yml
  ```

 You can edit the config of each of these streams within the `build/multi_instance` directory. To generate the consolidated `docker compose` and `eii_config.json` file, rerun the `builder.py` command.

  > **Note:**
  >
  > - The multi-instance feature support of Builder works only for the video pipeline that is the **usecases/video-streaming.yml** and **video-streaming-evam.yml** use case and not with any other use case yml files like **usecases/video-streaming-storage.yml** and so on. Also, it doesn't work for cases without the `-f` switch. The previous example will work with any positive number for `-v`. To learn more about using the multi-instance feature with the DiscoverHistory tool, see [Multi-instance feature support for the builder script with the DiscoverHistory tool](tools/DiscoverHistory/README.md#multi-instance-feature-support-for-the-builder-script-with-the-discoverhistory-tool).
  > - If you are running the multi-instance config for the first time, it is recommended not to change the default `config.json` file and the `docker-compose.yml` file in the `EdgeVideoAnalyticsMicroservice/eii` directory.
  > - If you are not running the multi-instance config for the first time, the existing `config.json` and `docker-compose.yml` files in the `build/multi_instance` directory will be used to generate the consolidated `eii-config.json` and `docker-compose` files.
  > - The `docker-compose.yml` files present within the `build/multi_instance` directory will have the following:
  >   - the updated service_name, container_name, hostname, AppName, ports and secrets for that respective instance.
  > - The `config.json file` in the `build/multi_instance` directory will have the following:
  >   - the updated Name, Type, Topics, Endpoint, PublisherAppname, ServerAppName, and AllowedClients for the interfaces section.
  >   - the incremented RTSP port number for the config section of that respective instance.
  > - Ensure that all containers are down before running the multi-instance configuration. Run the `docker-compose down` command before running the `builder.py` script for the multi-instance configuration.

##### Generate Benchmarking Config Using Builder

To provide a different set of `docker-compose.yml` and `config.json` files than those found in each service directory, use the `-d` or the `override directory` flag. The `-d` flag instructs the program to look in the specified directory for the necessary set of files.

For example, to pick files from a directory named benchmarking, you can run the following command:

  ```sh
     python3 builder.py -d benchmarking
  ```

> **Note:**
>
> - If you use the override directory feature of the builder then include all the 3 files mentioned in the previous example. If you do not include a file in the override directory, then the Builder will omit that service in the final config that is generated.
> - Adding the `AppName` of the subscriber container or client container in the `subscriber_list of builder_config.json` allows you to spawn a single subscriber container or client container that is subscribing or receiving on multiple publishers or server containers.
> - Multiple containers specified by the `-v` flag is spawned for services that are not mentioned in the `subscriber_list`. For example, if you run Builder with `–v 3` option and `Visualizer` is not added in the `subscriber_list` of `builder_config.json` then 3 instances of Visualizer are spawned. Each instance subscribes to 3 EdgeVideoAnalyticsMicroservice services. If Visualizer is added in the `subscriber_list` of `builder_config.json`, a single Visualizer instance subscribing to 3 multiple EdgeVideoAnalyticsMicroservice is spawned.

#### Task 3: Build and Run the Edge Insights for Industrial Video and Time Series Use Cases

  > **Note:**
  >
  > - For running the EII services in the IPC mode, ensure that the same user is mentioned in the publisher services and subscriber services.
  > - If the publisher service is running as root such as `EVAM`, then the subscriber service should also run as root. For example, in the `docker-compose.yml`file, if you have specified `user: ${EII_UID}` in the publisher service, then specify the same `user: ${EII_UID}` in the subscriber service. If you have not specified a user in the publisher service, then don't specify the user in the subscriber service.
  > - If services need to be running in multiple nodes in the TCP mode of communication, msgbus subscribers, and clients of `AppName` are required to configure the `EndPoint` in `config.json` with the `HOST_IP` and the `PORT` under `Subscribers/Publishers` or `Clients/Servers` interfaces section.
  > - Ensure that the port is being exposed in the `docker-compose.yml` of the respective `AppName`.
  > For example, if the `"EndPoint": <HOST_IP>:65114` is configured in the `config.json` file, then expose the port `65114` in the `docker-compose.yml` file of the `ia_edge_video_analytics_microservice` service.

  ```yaml
    ia_edge_video_analytics_microservice:
      ...
      ports:
        - 65114:65114
  ```

Run all the following EII build and commands from the `[WORKDIR]/IEdgeInsights/build/` directory.
EII supports the following use cases to run the services mentioned in the `docker_compose.yml` file. Refer to the [Task 2](#task-2-generate-deployment-and-configuration-files) to generate the `docker_compose.yml` file for a specific use case. For more information and configuration, refer to the `[WORK_DIR]/IEdgeInsights/README.md` file.

##### Independent building and deployment of services

- All the EII services are aligning with the Microservice architecture principles of being Independently buildable and deployable.
- Independently buildable and deployable feature is useful in allowing users to pick and choose only one service to build or deploy.
- If one wants to run two or more microservices, we recommend to use the use-case driven approach as mentioned in [Generate Consolidated Files for a Subset of Edge Insights for Industrial Services](#generate-consolidated-files-for-a-subset-of-Edge-insights-for-industrial-services).
- The Independently buildable and deployable feature allows the users to build the individual service at the directory level and also allows the users to deploy the service in either of the two ways:
    1) Without ConfigMgrAgent dependency:
      - Deployment without ConfigMgrAgent dependency is only available in DEV mode where we make use of the ConfigMgr library config file APIs, by setting the `READ_CONFIG_FROM_FILE_ENV` value to `true` in the [.env](build/.env) file.

    >> **NOTE:** We recommend the users to follow this simpler docker-compose deployment approach while adding in new services or debugging the existing service.

    2) With ConfigMgrAgent dependency:
      - Deployment with ConfigMgrAgent dependency is available in both DEV and PROD mode where we set the `READ_CONFIG_FROM_FILE_ENV` value to `false` in the [.env](build/.env) file and make use of the [ConfigMgrAgent](ConfigMgrAgent/docker-compose.yml) and the [builder.py](build/builder.py) to deploy the service.

    >> **NOTE:** We recommend the users to follow the earlier use-case driven approach mentioned in [Generate Consolidated Files for a Subset of Edge Insights for Industrial Services](#generate-consolidated-files-for-a-subset-of-Edge-insights-for-industrial-services), when they want to deploy more than one microservice.

##### Build the Edge Insights for Industrial Stack

> **Note:**
>
> - This is an optional step, if you want to use the EII pre-built container images and not build from source. For more details, refer to [List of Distributed EII Services](#list-of-distributed-eii-services)

Run the following command to build all EII services in the `build/docker-compose.yml` along with the base EII services.

```sh
docker-compose build
```

If any of the services fails during the build, then run the following command to build the service again:

```sh
docker-compose build --no-cache <service name>
```

##### Run Edge Insights for Industrial Services

> **Note:**
> Ensure to run `docker-compose down` from the [build](build) directory before you bring up the EII stack. This helps to remove running containers and avoid any sync issues where other services have come up before `ia_configmgr_agent` container has completed the provisioning step.
> If the images tagged with the `EII_VERSION` label, as in the [build/.env](build/.env) do not exist locally in the system but are available in the Docker Hub, then the images will be pulled during the `docker-compose up`command.

###### Provision Edge Insights for Industrial

The EII provisioning is taken care by the `ia_configmgr_agent` service that gets launched as part of the EII stack. For more details on the ConfigMgr Agent component, refer to the [Readme](ConfigMgrAgent/README.md).

###### Start Edge Insights for Industrial in Dev Mode

> **Note:**
>
> - By default, EII is provisioned in the secure mode.
> - It is recommended not to use EII in the Dev mode in a production environment. In the Dev mode, all security features, communication to and from the etcd server over the gRPC protocol, and the communication between the EII services/apps over the ZMQ protocol are disabled.
> - By default, the EII empty certificates folder [Certificates]([WORKDIR]/IEdgeInsights/build/Certificates]) will be created in the DEV mode. This happens because of docker bind mounts but it is not an issue.
> - The `EII_INSTALL_PATH` in the [build/.env](build/.env) remains protected both in the DEV and the PROD mode with the Linux group permissions.

Starting EII in the Dev mode eases the development phase for System Integrators (SI). In the Dev mode, all components communicate over non-encrypted channels. To enable the Dev mode, set the environment variable `DEV_MODE` to `true` in the `[WORK_DIR]/IEdgeInsights/build/.env` file. The default value of this variable is `false`.

To provision EII in the developer mode, complete the following steps:

1. Update `DEV_MODE=true` in `[WORK_DIR]/IEdgeInsights/build/.env`.
2. Rerun the `build/builder.py` to regenerate the consolidated files.

###### Start Edge Insights for Industrial in Profiling Mode

The Profiling mode is used for collecting the performance statistics in EII. In this mode, each EII component makes a record of the time needed for processing any single frame. These statistics are collected in the visualizer where System Integrators (SIs) can see the end-to-end processing time and the end-to-end average time for individual frames.

To enable the Profiling mode, in the `[WORK_DIR]/IEdgeInsights/build/.env` file, set the environment variable `PROFILING` to `true`.

###### Run Provisioning Service and Rest of the Edge Insights for Industrial Stack Services

> **Note**:
>
> - After the EII services starts, you can use the [Etcd UI](./ConfigMgrAgent/README.md#etcd-ui) web interface to make the changes to the EII service configs or interfaces keys.
> - in the DEV and the PROD mode, if the EII services come before the [Config Manager Agent](ConfigMgrAgent/README.md) service, then they would be in the restarting mode with error logs such as `Config Manager initialization failed...`. This is due to the single step deployment to support the independent deployment of the EII services, where services can come in a random order and start working when the dependent service comes up later. In one to two minutes, all the EII services should show the status as `running` when `Config Manager Agent` service starts up.
> - To build the common libs and generate needed artifacts from source and use it for building the EII services, refer [common/README.md](common/README.md#libs-package-generation).

```sh
docker-compose up -d
```

On successful run, you can open the web visualizer in the Chrome browser at https://<HOST_IP>:3000. The `HOST_IP` corresponds to the IP of the system on which the visualization service is running.

## Push the Required Edge Insights for Industrial Images to Docker Registry

> **Note:**
> By default, if `DOCKER_REGISTRY` is empty in [build/.env](build/.env) then the images are published to hub.docker.com. Ensure to remove `edgeinsights/` org from the image names while pushing to Docker Hub. Repository names or image names with multiple slashes are not supported. This limitation doesn't exist in other docker registries like the Azure Container Registry (ACR), Harbor registry, and so on.

Run the following command to push all the EII service docker images in the `build/docker-compose.yml`. Ensure to update the `DOCKER_REGISTRY` value in the [.env](build/.env) file.

```sh
docker-compose push
```

## List of EII Services

Based on requirement, you can include or exclude the following EII services in the `[WORKDIR]/IEdgeInsights/build/docker-compose.yml` file:

- Provisioning Service - This service is a prerequisite and cannot be excluded from the `docker-compose.yml` file.
  - [ConfigMgrAgent](ConfigMgrAgent/README.md)
- Common EII services for Video and Timeseries Analytics pipeline services
  - [DataStore](DataStore/README.md)
  - [OpcuaExport](OpcuaExport/README.md) - Optional service to read from the EdgeVideoAnalyticsMicroservice container to publish data to opcua clients.
  - [RestDataExport](RestDataExport/README.md) - Optional service to read the metadata and the image blob from the from the Data store service.
  - [Visualizer](Visualizer/README_EII.md)
- Video Analytics pipeline services
  - [EdgeVideoAnalyticsMicroservice](EdgeVideoAnalyticsMicroservice/README.md)
  - [EdgeToAzureBridge](EdgeToAzureBridge/README_EII.md)
  - [FactoryControlApp](FactoryControlApp/README.md) - Optional service to read from the EdgeVideoAnalyticsMicroservice container if you want to control the light based on the defective or non-defective data
- Timeseries Analytics pipeline services
  - [Telegraf](Telegraf/README.md)
  - [Kapacitor](Kapacitor/README.md)
  - [ZMQ Broker](ZmqBroker/README.md)

## Adding New Services to EII Stack

This section provides information about adding a service, subscribing to the [EdgeVideoAnalyticsMicroservice](./EdgeVideoAnalyticsMicroservice), and publishing it on a new port.
Add a service to the EII stack as a new directory in the [IEdgeInsights](./) directory. The Builder registers and runs any service present in its own directory in the [IEdgeInsights](./) directory. The directory should contain the following:

- A `docker-compose.yml` file to deploy the service as a docker container. The `AppName` is present in the `environment` section in the `docker-compose.yml` file. Before adding the `AppName` to the main `build/eii_config.json`, it is appended to the `config` and `interfaces` as `/AppName/config` and `/AppName/interfaces`.
- A `config.json` file that contains the required config for the service to run after it is deployed. The `config.json` consists of the following:
  - A `config` section, which includes the configuration-related parameters that are required to run the application.
  - An `interfaces` section, which includes the configuration of how the service interacts with other services of the EII stack.

> **Note**
> For more information on adding new EII services, refer to the EII sample apps at [Samples](Samples/README.md) written in C++, Python, and Golang using the EII core libraries.

The following example shows:

- How to write the **config.json** for any new service
- Subscribe to **EdgeVideoAnalyticsMicroservice**
- Publish on a new port

```javascript
    {
        "config": {
            "paramOne": "Value",
            "paramTwo": [1, 2, 3],
            "paramThree": 4000,
            "paramFour": true
        },
        "interfaces": {
            "Subscribers": [
                {
                    "Name": "default",
                    "Type": "zmq_tcp",
                    "EndPoint": "127.0.0.1:65114",
                    "PublisherAppName": "EdgeVideoAnalyticsMicroservice",
                    "Topics": [
                        "edge_video_analytics_results"
                    ]
                }
            ],
            "Publishers": [
                {
                    "Name": "default",
                    "Type": "zmq_tcp",
                    "EndPoint": "127.0.0.1:65113",
                    "Topics": [
                        "publish_stream"
                    ],
                    "AllowedClients": [
                        "ClientOne",
                        "ClientTwo",
                        "ClientThree"
                    ]
                }
            ]
        }
    }
```

The `config.json` file consists of the following key and values:

- value of the `config` key is the config required by the service to run.
- value of the `interfaces` key is the config required by the service to interact with other services of EII stack over the Message Bus.
- the `Subscribers` value in the `interfaces` section denotes that this service should act as a subscriber to the stream being published by the value specified by `PublisherAppName` on the endpoint mentioned in value specified by `EndPoint` on topics specified in value of `Topic` key.
- the `Publishers` value in the `interfaces` section denotes that this service publishes a stream of data after obtaining and processing it from `EdgeVideoAnalyticsMicroservice`. The stream is published on the endpoint mentioned in value of `EndPoint` key on topics mentioned in the value of `Topics` key.
- the services mentioned in the value of `AllowedClients` are the only clients that can subscribe to the published stream, if it is published securely over the Message Bus.

> **Note:**
>
> - Like the interface keys, EII services can also have `Servers` and `Clients` interface keys.
> - For more information on the `interfaces` key responsible for the Message Bus endpoint configuration, refer to [common/libs/ConfigMgr/README.md#interfaces](common/libs/ConfigMgr/README.md#interfaces).
> - For the etcd secrets configuration, in the new EII service or app `docker-compose.yml` file, add the following volume mounts with the right `AppName` env value:
>
> ```yaml
> ...
>  volumes:
>    - ./Certificates/[AppName]:/run/secrets/[AppName]:ro
>    - ./Certificates/rootca/cacert.pem:/run/secrets/rootca/cacert.pem:ro
> ```

## Video Pipeline Analytics

This section provides more information about working with the video pipeline.

#### Enable Camera based Ingestion

The Edge Video Analytics Microservice supports different types of cameras. For more details about camera configurations, refer the [README](./EdgeVideoAnalyticsMicroservice/eii/README.md#camera-configurations).

#### Integrate Python UDF

You can integrate any python UDF with the Edge Video Analytics Microservice using the volume mount method.
For more details about python UDF integration, refer the [README](./EdgeVideoAnalyticsMicroservice/eii/README.md#integrate-python-udf-with-edgevideoanalyticsmicroservice-service)

#### Use Video Accelerators in Edge Video Analytics Microservice

Edge Video Analytics Microservice supports running inference on CPU and GPU devices by accepting the device value ("CPU"|"GPU"), part of the udf object configuration in the udfs key.
The device field in the UDF config of udfs key in the EdgeVideoAnalyticsMicroservice configs needs to be updated.
Refer these steps for running [Edge Video Analytics Microservice on a GPU device](./EdgeVideoAnalyticsMicroservice/eii/README.md#running-edgevideoanalyticsmicroservice-on-a-gpu-device).

## Time Series Analytics

For time series data, a sample analytics flow uses Telegraf for ingestion, Influx DB for storage, and Kapacitor for classification. This is demonstrated with an MQTT-based ingestion of sample temperature sensor data and analytics with a Kapacitor UDF that detects threshold for the input values.
The services mentioned in the [build/usecases/time-series.yml](build/usecases/time-series.yml) file will be available in the consolidated `docker-compose.yml` and consolidated `build/eii_config.json` of the EII stack for the time series use case when built via `builder.py` as called out in previous steps.
This will enable building of the Telegraf and the Kapacitor based analytics containers.
For more details on enabling this mode, refer to the [Kapacitor/README.md](Kapacitor/README.md)
The sample temperature sensor can be simulated using the MQTT publisher. For more information, refer to the [tools/mqtt/README.md](tools/mqtt/README.md).

## Time Series Python UDFs Development

In the `DEV` mode, the Python UDFs are volume mounted in the Kapacitor container image as seen in its `docker-compose-dev.override.yml` file. You can update the UDFs on the host machine and see the changes in Kapacitor. You can do this by restarting the Kapactior container. Rebuilding the Kapacitor container image is not required.

>**Note**: To enable the `DEV` mode, in the `[WORK_DIR]/IEdgeInsights/build/.env` set `DEV_MODE=true`.

## Edge Insights for Industrial Multi-node Cluster Deployment

### With K8s Orchestrator

You can use any of the following options to deploy EII on a multi-node cluster:

- [`Recommended`] For deploying through ansible playbook on multiple nodes automatically, refer to [build/ansible/README.md](build/ansible/README.md#deploying-eii-using-helm-in-kubernetes-k8s-environment)
- For information about using helm charts to provision the node and deploy the EII services, refer to [build/helm-eii/README.md](build/helm-eii/README.md)

## Edge Insights for Industrial Tools

The EII stack consists of the following set of tools that also run as containers:

- Benchmarking
  - [Video Benchmarking](tools/Benchmarking/video-benchmarking-tool/README.md)
  - [Time series Benchmarking](tools/Benchmarking/time-series-benchmarking-tool/README.md)
- [DiscoverHistory](tools/DiscoverHistory/README.md)
- [EmbPublisher](tools/EmbPublisher/README.md)
- [EmbSubscriber](tools/EmbSubscriber/README.md)
- [HttpTestServer](tools/HttpTestServer/README.md)
- [MQTT](tools/mqtt/README.md)
- [TimeSeriesProfiler](tools/TimeSeriesProfiler/README.md)
- [VideoProfiler](tools/VideoProfiler/README.md)

## Edge Insights for Industrial Uninstaller

The EII uninstaller script automatically removes all the EII Docker configuration that is installed on a system. The uninstaller performs the following tasks:

- Stops and removes all the EII running and stopped containers.
- Removes all the EII docker volumes.
- Removes all the EII docker images \[Optional\]
- Removes all EII install directory

To run the uninstaller script, run the following command from the `[WORKDIR]/IEdgeInsights/build/` directory:

```sh
./eii_uninstaller.sh -h
```

Usage: ./eii_uninstaller.sh [-h] [-d]
This script uninstalls the previous EII version.
Where:
    -h show the help
    -d triggers the deletion of docker images (by default it will not trigger)
Example:

- Run the following command to delete the EII containers and volumes:

  ```sh
      ./eii_uninstaller.sh
  ```

- Run the following command to delete the EII containers, volumes, and images:

  ```sh
    EII_VERSION=3.0.0 ./eii_uninstaller.sh -d
  ```

The commands in the example will delete the version 2.4 EII containers, volumes, and all the docker images.

## Debugging Options

Perform the following steps for debugging:

1. Run the following command to check if all the EII images are built successfully:

    ```sh
    docker images|grep ia
    ```

2. You can view all the dependency containers and the EII containers that are up and running. Run the following command to check if all containers are running:

    ```sh
    docker ps
    ```

3. Ensure that the proxy settings are correctly configured and restart the docker service if the build fails due to no internet connectivity.
4. Run the `docker ps` command to list all the enabled containers that are included in the `docker-compose.yml` file.
5. From edge video analytics microservice>visualizer, check if the default video pipeline with EII is working fine.
6. The `/opt/intel/eii` root directory gets created - This is the installation path for EII:
     - `data/` - stores the backup data for persistent imagestore and influxdb
     - `sockets/` - stores the IPC ZMQ socket files

The following table displays useful docker-compose and docker commands:

|  Command  |  Description |
| :---:     | :---:        |
|   `docker-compose build`| Builds all the service containers|
| `docker-compose build [serv_cont_name]`| Builds a single service container      |
| `docker-compose down`      | Stops and removes the service containers|
| `docker-compose up -d`      | Brings up the service containers by picking the changes done in the `docker-compose.yml` file|
| `docker ps`      | Checks the running containers|
| `docker ps -a`       | Checks the running and stopped containers      |
| `docker stop $(docker ps -a -q)`      | Stops all the containers      |
| `docker rm $(docker ps -a -q)`      | Removes all the containers. This is useful when you run into issue of already container is in use|
| `[docker compose cli]`      | For more information refer to the [docker documentation](https://docs.docker.com/compose/reference/overview/)      |
| `[docker compose reference]`      | For more information refer to the [docker documentation](https://docs.docker.com/compose/compose-file/)      |
|`[docker cli]`       | For more information refer to the [docker documentation](https://docs.docker.com/engine/reference/commandline/cli/#configuration-files)      |
| `docker-compose run --no-deps [service_cont_name]`| To run the docker images separately or one by one. For example: `docker-compose run --name ia_edge_video_analytics_microservice --no-deps   ia_edge_video_analytics_microservice` to run the EdgeVideoAnalyticsMicroservice container and the switch `--no-deps` will not bring up its dependencies mentioned in the `docker-compose` file. If the container does not launch, there could be some issue with the entrypoint program. You can override by providing the extra switch `--entrypoint /bin/bash` before the service container name in the `docker-compose run` command. This will let you access the container and run the actual entrypoint program from the container's terminal to root cause the issue. If the container is running and you want to access it then, run the command: `docker-compose exec [service_cont_name] /bin/bash` or `docker exec -it [cont_name] /bin/bash`|
| `docker logs -f [cont_name]`| Use this command to check logs of containers      |
| `docker-compose logs -f` | To see all the docker-compose service container logs at once |

## Web Deployment Tool

Web Deployment Tool is a GUI tool to facilitate EII configuration and deployment for single and multiple video streams. 

Web Deployment Tool features include:

- Offers GUI interface to try out EII stack for video use case
- Supports multi-instance feature of EVAM service
- Supports an easy way to use or modify existing UDFs or add new UDFs
- Supports preview to visualize the analyzed frames
- Supports deployment of the tested configuration on other remote nodes via ansible

To learn about launching and using the Web Deployment Tool, refer to the following:

- [Web Deployment Tool back end ReadMe](DeploymentToolBackend/README.md)
- [Web Deployment Tool front end ReadMe](DeploymentToolFrontend/README.md)

## Troubleshooting Guide

- For any troubleshooting tips related to the EII configuration and installation, refer to the [TROUBLESHOOT.md](./TROUBLESHOOT.md) guide.
- Since all the EII services are independently buildable and deployable when we do a `docker-compose up` for all EII microservices, the order in 
  which they come up is not controlled. Having said this, there are many publishers and subscriber microservices in EII middleware, hence, 
  its possible that publisher comes up before subscriber or there can be a slght time overlap wherein the subscriber can come up just after 
  publisher comes up. Hence, in these scenarios its a possibility that the data published by publisher can be lost as subscriber would not be 
  up to receive all the published data. So, the solution to address this is to restart the publisher after we are sure that the intended subscriber is up. 
- If you observe any issues with the installation of the Python package, then as a workaround you can manually install the Python packages by running the following commands:
  
  ```sh
  cd [WORKDIR]/IEdgeInsights/build
  # Install requirements for builder.py
  pip3 install -r requirements.txt
  ```

  > **Note:**
  > To avoid any changes to the Python installation on the system, it is recommended that you use a Python virtual environment to install the Python packages. For more information on setting up and using the Python virtual environment, refer to [Python virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/).
>>>>>>> first commit
