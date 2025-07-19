# Event Photo Upload Web App

This project is a containerized Python web application that allows users to upload photos during an event. No authentication is required. Uploaded photos are saved directly to an Azure Storage Account container. The app is designed for easy deployment on Azure. I was asked to create this the morning of the event... 

## Methodology
1. Create web application that connects Azure Blob Storage and uploads photos with event branding, super simple.
2. Containerise.
3. Build and test locally.
4. Add workflow to build and push container to Azure Container registry.
5. Create a new Azure Container App and Azure Container Environment to pull image from Azure Container Registry and provide access via ingress.
6. Create a poster to the public fqdn via QR code.
7. Enjoy success.

## Features
- Simple web interface for uploading photos
- No login or authentication required
- Photos are stored in Azure Blob Storage
- Containerized for easy deployment

## Getting Started
Create and populate `.env` file based on `.env.example`. Use `cmd + shift + p` to open command palette within VS Code. Then use `Tasks: Run Task` to run `Build Docker Container` and the subsequent `Run Docker Container` tasks to build and run locally.
