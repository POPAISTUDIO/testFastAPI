#!/bin/bash

# Install and manage FastAPI Image Generation Service as systemd service

SERVICE_NAME="fastapi-image-service"
SERVICE_FILE="fastapi-image-service.service"
CURRENT_DIR=$(pwd)

echo "FastAPI Image Generation Service Installer"
echo "=========================================="

# Function to install the service
install_service() {
    echo "Installing $SERVICE_NAME service..."
    
    # Copy service file to systemd directory
    sudo cp "$SERVICE_FILE" /etc/systemd/system/
    
    # Reload systemd daemon
    sudo systemctl daemon-reload
    
    # Enable the service
    sudo systemctl enable "$SERVICE_NAME"
    
    echo "Service installed and enabled successfully!"
    echo "You can start it with: sudo systemctl start $SERVICE_NAME"
    echo "Check status with: sudo systemctl status $SERVICE_NAME"
}

# Function to start the service
start_service() {
    echo "Starting $SERVICE_NAME service..."
    sudo systemctl start "$SERVICE_NAME"
    sudo systemctl status "$SERVICE_NAME"
}

# Function to stop the service
stop_service() {
    echo "Stopping $SERVICE_NAME service..."
    sudo systemctl stop "$SERVICE_NAME"
    sudo systemctl status "$SERVICE_NAME"
}

# Function to restart the service
restart_service() {
    echo "Restarting $SERVICE_NAME service..."
    sudo systemctl restart "$SERVICE_NAME"
    sudo systemctl status "$SERVICE_NAME"
}

# Function to uninstall the service
uninstall_service() {
    echo "Uninstalling $SERVICE_NAME service..."
    
    # Stop and disable the service
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
    
    # Remove service file
    sudo rm -f /etc/systemd/system/"$SERVICE_FILE"
    
    # Reload systemd daemon
    sudo systemctl daemon-reload
    
    echo "Service uninstalled successfully!"
}

# Function to show service status
show_status() {
    echo "Service status:"
    sudo systemctl status "$SERVICE_NAME"
}

# Function to show logs
show_logs() {
    echo "Service logs:"
    sudo journalctl -u "$SERVICE_NAME" -f
}

# Main script logic
case "$1" in
    install)
        install_service
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    uninstall)
        uninstall_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {install|start|stop|restart|uninstall|status|logs}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and enable the service"
        echo "  start     - Start the service"
        echo "  stop      - Stop the service"
        echo "  restart   - Restart the service"
        echo "  uninstall - Uninstall the service"
        echo "  status    - Show service status"
        echo "  logs      - Show service logs"
        exit 1
        ;;
esac 