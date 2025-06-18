package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;

@Service
public class RabbitMQListener {

    @RabbitListener(queues = "DF.pdf")
    public void receiveMessage(String message) {
        System.out.println("APR PDF Generator received a message from the DF.pdf queue: " + message);
    }
}
