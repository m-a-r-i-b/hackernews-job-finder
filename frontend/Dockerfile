# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory
WORKDIR /app

# # Copy the package.json and package-lock.json files
# COPY package*.json ./

# Copy the rest of the application code
COPY . .

# Install any needed packages
RUN npm install

# Command to run the React app
CMD ["npm", "start"]
