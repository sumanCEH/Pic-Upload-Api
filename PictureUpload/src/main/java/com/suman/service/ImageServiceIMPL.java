package com.suman.service;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.suman.entity.Image;
import com.suman.repository.ImageRepository;

@Service
public class ImageServiceIMPL implements ImageService {

	@Autowired
	private ImageRepository imageRepository;


	@Override
	public String saveImage(MultipartFile file) throws IOException {
		Image image = new Image();
		image.setImage(file.getBytes());
		imageRepository.save(image);
		return "image upload sucessfully";
	}

	@Override
	public byte[] getImageById(long id) throws RuntimeException {
        // Use imageRepository.findById to retrieve the image by ID
        // Assuming that the findById method returns an Optional<Image>
        // You can customize this based on your actual repository methods
        Image image = imageRepository.findById(id).orElse(null);

        if (image != null) {
            return image.getImage();
        } else {
            throw new RuntimeException("Image not found with id: " + id);
        }
    }
	
	 
}
