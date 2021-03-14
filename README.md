# krwordcloud

A korean local news wordcloud service with over-stack
(WIP)

## How to install(Not working)

1. Install in Local machine(Single cluster)

    ```bash
    # Install kubernetes 
    # Minikube guide - https://minikube.sigs.k8s.io/docs/start/

    # Install helm
    # Helm - https://helm.sh/docs/intro/install/ 

    # Install nodejs
    # n guide - https://github.com/tj/n#installation

    # Clone the project repository
    git clone https://github.com/hoongeun/krwordcloud
    cd ./krwordcloud/helm

    # helmvalues
    npx helmvalues build

    # apply to kubernetes
    helm install krwordcloud ./
    ```

2. Options2) Install in virtual machines(Multi cluster)

   ```bash
    # Install Vagrant
    # guide - https://www.vagrantup.com/downloads

    # Clone the project repository
    git clone https://github.com/hoongeun/krwordcloud

    # Move to krwordcloud's vagrant directory
    cd ./krwordcloud/vagrant

    # optional - destory all staging virtualmachines
    vagrant destroy -f

    # vagrant up
    vagrant up
    ```

3. Options3, Will suppport) Install in native cluster(Multi cluster)

## Stack

* application:
  * front: react(typescript)
  * backend: spring(kotlin)
* database:
  * couchbase: keyword-score(proccessed data) store
  * hdfs: article storage with orc(Optimized row columnar)
* datamining: spark-operator(pyspark)
  * keyword extracting algorithm: [krwordrank](https://github.com/lovit/KR-WordRank)
* datacrawler: modified [korean_news_crawler](https://github.com/lumyjuwon/KoreaNewsCrawler)
* orchestration: kubernetes, helm, vagrant
* cd: argocd
* monitoring: prometheus, grafana
* scheduler: airflow
* message queue: kafka(confluent-platform)

## Peoples
* [Hoongeun Cho](https://github.com/hoongeun) (me@hoongeun.com): Architect, Project management, orchestration, application, spark

* [Jinseong Choi](https://github.com/ysfactory): airflow
