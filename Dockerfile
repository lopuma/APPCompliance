# Slim version of Python
FROM python:3.8.12-slim

# Download Package Inf/home/esy9f47u/Alvaro/Desarrollo/APPComplianceormation
RUN yum update

# Install Tkinter
RUN yum install tk

# Commands to run Tkinter application
CMD ["/Alvaro/Desarrollo/APPCompliance/Compliance.py"]
ENTRYPOINT ["python3"]
