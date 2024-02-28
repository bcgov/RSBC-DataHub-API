package ca.bc.gov.open.rsbc.mailit.mail.mappers;

import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailObject;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;
import org.springframework.mail.SimpleMailMessage;

import java.util.List;

@Mapper
public interface SimpleMessageMapper {

    @Mapping(target = "from", source = "from.email")
    @Mapping(target = "replyTo", ignore = true)
    @Mapping(target = "to", source = "to", qualifiedByName = "emailObjectCollectionToStringArray")
    @Mapping(target = "cc", source = "cc", qualifiedByName = "emailObjectCollectionToStringArray")
    @Mapping(target = "bcc", ignore = true)
    @Mapping(target = "sentDate", ignore = true)
    @Mapping(target = "subject", source="subject")
    @Mapping(target = "text", source="content.value")
    SimpleMailMessage toSimpleMailMessage(EmailRequest emailRequest);

    @Named("emailObjectCollectionToStringArray")
    default String[] emailObjectCollectionToStringArray(List<EmailObject> emailObject) {

        if(emailObject == null) return new String[0];

        return emailObject.stream().map(x -> x.getEmail()).toArray(size -> new String[size]);

    }

}
