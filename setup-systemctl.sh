#!/bin/bash

# Setup script for Raichuu systemctl service
# Run this script on your server to install the systemctl service

echo "🚀 Setting up Raichuu systemctl service..."

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script with sudo:"
    echo "sudo ./setup-systemctl.sh"
    exit 1
fi

# Copy the service file to systemd directory
echo "📋 Copying service file to /etc/systemd/system/"
cp raichuu.service /etc/systemd/system/

# Reload systemd to recognize the new service
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable the service to start on boot
echo "✅ Enabling service to start on boot..."
systemctl enable raichuu

# Start the service
echo "🚀 Starting Raichuu service..."
systemctl start raichuu

# Check service status
echo "📊 Service status:"
systemctl status raichuu --no-pager

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔧 Useful commands:"
echo "  sudo systemctl start raichuu     # Start the service"
echo "  sudo systemctl stop raichuu      # Stop the service"
echo "  sudo systemctl restart raichuu   # Restart the service"
echo "  sudo systemctl status raichuu    # Check service status"
echo "  sudo systemctl logs raichuu      # View service logs"
echo ""
echo "🌐 Your website should now be running!"
