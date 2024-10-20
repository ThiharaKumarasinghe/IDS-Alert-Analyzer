import React, { useState } from "react";
import bannerImage from "/bannerImage.png";
import { motion } from "framer-motion";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.5, staggerChildren: 0.5 },
  },
};

const PCAP_Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith(".pcap")) {
      setSelectedFile(file);
    } else {
      alert("Please select a valid .pcap file");
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a .pcap file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true); // Show loading state

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data); // Store the result from the backend
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setLoading(false); // Hide loading state
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      {/* Left side */}
      <motion.div
        className="w-full md:w-1/2 flex-col flex space-y-9"
        initial={{ x: 100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        variants={containerVariants}
      >
        <h2 className="text-xl font-bold text-purple">Welcome to...</h2>
        <h1 className="text-5xl font-extrabold text-blue-950">
          IDS Alerts Analyser
        </h1>
        <p>
          This tool allows you to upload and analyze your PCAP (Packet Capture)
          files. Using advanced processing techniques, it will provide detailed
          insights and explanations of the network traffic captured in your
          files.
        </p>
        <p className="font-bold">
          Get started by uploading a PCAP file to see the analysis results.
        </p>

        <input
          type="file"
          accept=".pcap" // Restrict to only .pcap files
          onChange={handleFileChange}
          className="file-input file-input-bordered w-full max-w-xs"
        />

        <button
          className="btn btn-neutral max-w-24 hover:scale-105"
          onClick={handleUpload}
        >
          Start
        </button>

        {/* Display loading message or result */}
        {loading ? (
          <div className="text-center text-lg text-blue-500">
            Analyzing the file, please wait...
          </div>
        ) : result ? (
          <div className="text-center text-lg text-green-500">
            Analysis Result: {result.message}
          </div>
        ) : null}
      </motion.div>

      {/* Right side */}
      <motion.div
        className="w-full md:w-1/2"
        animate={{ scale: [1, 1.05, 1] }} // Zoom in and out
        transition={{ duration: 5, repeat: Infinity }}
      >
        <img src={bannerImage} alt="Banner" className="w-full object-contain" />
      </motion.div>
    </div>
  );
};

export default PCAP_Upload;
