# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the application code
COPY . .


RUN ls

# Command to run the React app
CMD ["npm","start"]
