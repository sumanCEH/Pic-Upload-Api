package com.suman.entity;

import java.util.Arrays;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;

@Entity
@Table(name="image_db")
public class Image {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Lob
	private byte[] image;
	
	public Image() {
		super();
		// TODO Auto-generated constructor stub
	}
	
	
	public Image(long id, byte[] image) {
		super();
		this.id = id;
		this.image = image;
	}
	

	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public byte[] getImage() {
		return image;
	}
	public void setImage(byte[] image) {
		this.image = image;
	}


	@Override
	public String toString() {
		return "Image [id=" + id + ", image=" + Arrays.toString(image) + "]";
	}
	

}
