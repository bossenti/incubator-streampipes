package org.streampipes.sdk.helpers;

import org.streampipes.model.grounding.JmsTransportProtocol;
import org.streampipes.model.grounding.KafkaTransportProtocol;
import org.streampipes.model.grounding.WildcardTopicDefinition;

public class Protocols {

  /**
   * Defines the transport protocol Kafka used by a data stream at runtime using a
   * {@link org.streampipes.model.grounding.SimpleTopicDefinition}.
   * @param kafkaHost The hostname of any Kafka broker
   * @param kafkaPort The port of any Kafka broker
   * @param topic The topic identifier
   * @return The {@link org.streampipes.model.grounding.KafkaTransportProtocol} containing URL and topic where data
   * arrives.
   */
  public static KafkaTransportProtocol kafka(String kafkaHost, Integer kafkaPort, String topic) {
    return new KafkaTransportProtocol(kafkaHost, kafkaPort, topic, kafkaHost, kafkaPort);
  }

  /**
   * Defines the transport protocol Kafka used by a data stream at runtime using a
   * {@link org.streampipes.model.grounding.WildcardTopicDefinition}
   * @param kafkaHost The hostname of any Kafka broker
   * @param kafkaPort The port of any Kafka broker
   * @param wildcardTopicDefinition The wildcard topic definition.
   * @return  The {@link org.streampipes.model.grounding.KafkaTransportProtocol} containing URL and topic where data
   * arrives.
   */
  public static KafkaTransportProtocol kafka(String kafkaHost, Integer kafkaPort, WildcardTopicDefinition
          wildcardTopicDefinition) {
    return new KafkaTransportProtocol(kafkaHost, kafkaPort, wildcardTopicDefinition);

  }

  /**
   * Defines the transport protocol Kafka used by a data stream at runtime.
   * @param jmsHost The hostname of any JMS broker
   * @param jmsPort The port of any JMS broker
   * @param topic The topic identifier
   * @return The {@link org.streampipes.model.grounding.KafkaTransportProtocol} containing URL and topic where data
   * arrives.
   */
  public static JmsTransportProtocol jms(String jmsHost, Integer jmsPort, String topic) {
    return new JmsTransportProtocol(jmsHost, jmsPort, topic);
  }
}
