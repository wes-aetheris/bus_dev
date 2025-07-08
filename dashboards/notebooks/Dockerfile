FROM jupyter/datascience-notebook:latest

USER root

# Install additional packages
RUN pip install --no-cache-dir \
    plotly==5.17.0 \
    requests==2.31.0 \
    websocket-client==1.7.0 \
    python-dotenv==1.0.0 \
    scipy==1.11.4 \
    seaborn==0.13.0

# Create data directory
RUN mkdir -p /home/jovyan/data
RUN chown -R jovyan:users /home/jovyan/data

USER jovyan

# Set working directory
WORKDIR /home/jovyan

# Copy notebooks
COPY *.ipynb /home/jovyan/

# Expose port
EXPOSE 8888

# Start Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"] 