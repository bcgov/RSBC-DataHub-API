package ca.bc.gov.open.pssg.rsbc.service;

import java.io.IOException;
import java.io.InputStream;

import ca.bc.gov.open.pssg.rsbc.exception.VirusDetectedException;

public interface ClamAvService {

    void scan(InputStream inputStream) throws VirusDetectedException;

    boolean ping() throws IOException;

}
