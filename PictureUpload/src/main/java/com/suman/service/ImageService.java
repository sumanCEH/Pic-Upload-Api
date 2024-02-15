package com.suman.service;

import java.io.IOException;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public interface ImageService {
	public String saveImage(MultipartFile file) throws IOException;

	public byte[] getImageById(long id) throws RuntimeException;

}
