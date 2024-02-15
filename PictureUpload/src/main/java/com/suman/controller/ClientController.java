package com.suman.controller;
import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;

import com.suman.service.ImageService;

@RestController
@RequestMapping("/user/profile")
public class ClientController {
    @Autowired
    private ImageService imageService;

    @GetMapping("/ping")
    public String hello_world(){
        return "Hello World!";
    }

    @PostMapping("/save")
    public String saveImage(@RequestParam("file")MultipartFile file) throws IOException{
    return imageService.saveImage(file);
    }
    
    @GetMapping("/image/{id}")
    public ResponseEntity<byte[]> getImageById(@PathVariable long id) throws RuntimeException {
        byte[] imageData = imageService.getImageById(id);

        // Assuming JPEG image. You can set appropriate content type based on your image type.
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.IMAGE_JPEG);

        return new ResponseEntity<>(imageData, headers, HttpStatus.OK);
    }
    }