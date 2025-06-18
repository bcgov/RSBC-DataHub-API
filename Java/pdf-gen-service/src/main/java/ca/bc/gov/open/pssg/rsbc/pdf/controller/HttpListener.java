package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HttpListener {

    @GetMapping("/renderpdf")
    public String renderPdf() {
        
        return "Render PDF called";
    }
}


