// uart_loopback_test.cpp
// Compile with: g++ -o uart_loopback_test uart_loopback_test.cpp

#include <iostream>
#include <string>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <sys/ioctl.h>

int test_uart_loopback(const std::string& port, int baud_rate = 115200, int timeout_seconds = 3) {
    struct termios tty;
    int fd;
    
    std::cout << "Testing loopback on " << port << " at " << baud_rate << " baud..." << std::endl;
    
    // Open the serial port
    fd = open(port.c_str(), O_RDWR | O_NOCTTY | O_SYNC);
    if (fd < 0) {
        std::cerr << "Error opening " << port << ": " << strerror(errno) << std::endl;
        return -1;
    }
    
    // Save original terminal settings
    if (tcgetattr(fd, &tty) != 0) {
        std::cerr << "Error from tcgetattr: " << strerror(errno) << std::endl;
        close(fd);
        return -1;
    }
    
    // Set terminal settings
    cfsetospeed(&tty, baud_rate);
    cfsetispeed(&tty, baud_rate);
    
    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;  // 8-bit chars
    tty.c_iflag &= ~IGNBRK;                      // Disable break processing
    tty.c_lflag = 0;                             // No signaling chars, no echo
    tty.c_oflag = 0;                             // No remapping, no delays
    tty.c_cc[VMIN] = 0;                          // Read doesn't block
    tty.c_cc[VTIME] = timeout_seconds * 10;      // 0.1 seconds read timeout per decisecond unit
    
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);      // Disable flow control
    tty.c_cflag |= (CLOCAL | CREAD);             // Enable reading, ignore modem ctrl lines
    tty.c_cflag &= ~(PARENB | PARODD);           // No parity
    tty.c_cflag &= ~CSTOPB;                      // 1 stop bit
    tty.c_cflag &= ~CRTSCTS;                     // Disable hardware flow control
    
    // Apply settings
    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        std::cerr << "Error from tcsetattr: " << strerror(errno) << std::endl;
        close(fd);
        return -1;
    }
    
    // Flush any existing data
    tcflush(fd, TCIOFLUSH);
    
    // Test message
    const char *test_msg = "UART Loopback Test\n";
    std::cout << "Sending: " << test_msg;
    
    // Write test message
    ssize_t written = write(fd, test_msg, strlen(test_msg));
    if (written < 0) {
        std::cerr << "Error writing to " << port << ": " << strerror(errno) << std::endl;
        close(fd);
        return -1;
    }
    
    // Allow time for loopback transmission
    usleep(100000);  // 100ms
    
    // Read response
    char buffer[256];
    memset(buffer, 0, sizeof(buffer));
    
    ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
    
    if (bytes_read > 0) {
        std::cout << "Received: " << buffer;
        std::cout << "Loopback test: SUCCESS" << std::endl;
    } else if (bytes_read == 0) {
        std::cout << "No data received." << std::endl;
        std::cout << "Loopback test: FAILED" << std::endl;
    } else {
        std::cerr << "Error reading from " << port << ": " << strerror(errno) << std::endl;
    }
    
    close(fd);
    return (bytes_read > 0) ? 0 : 1;
}

int main(int argc, char* argv[]) {
    std::string port = "/dev/ttyS4";  // Default port
    int baud_rate = 115200;
    int timeout = 3;
    
    // Parse command line arguments
    if (argc > 1) {
        port = argv[1];
    }
    
    // Check for baud rate argument
    for (int i = 1; i < argc - 1; i++) {
        if (std::string(argv[i]) == "-b" || std::string(argv[i]) == "--baud") {
            baud_rate = std::stoi(argv[i+1]);
        }
        else if (std::string(argv[i]) == "-t" || std::string(argv[i]) == "--timeout") {
            timeout = std::stoi(argv[i+1]);
        }
    }
    
    return test_uart_loopback(port, baud_rate, timeout);
}