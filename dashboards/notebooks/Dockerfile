FROM jupyter/datascience-notebook:latest

USER root

# Install additional dependencies
RUN pip install --no-cache-dir \
    plotly==5.17.0 \
    scikit-learn==1.3.2 \
    requests==2.31.0 \
    seaborn==0.12.2

# Create working directory
WORKDIR /home/jovyan/work

# Copy notebook and tools
COPY sensor_analysis.ipynb ./
COPY ace_tools.py ./

# Set permissions
RUN chown -R jovyan:users /home/jovyan/work

USER jovyan

# Expose port
EXPOSE 8888

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8888/api/status || exit 1

# Start Jupyter
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
