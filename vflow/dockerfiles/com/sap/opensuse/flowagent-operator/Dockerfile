FROM §/com.sap.datahub.linuxx86_64/flowagent-operator:2.6.61

#COPY run.sh /vrep/vflow/subengines/com/sap/dh/flowagent/run.sh
#COPY flowAgent.ini /usr/sap/flowagent/flowAgent.ini
USER root

RUN usermod -aG root flowagent

#USER flowagent

#RUN usermod -a -G root flowagent
#COPY bootstrap_operator.sh /usr/sap/flowagent/bootstrap_operator.sh