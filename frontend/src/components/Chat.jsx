import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import Message from './Message';
import Input from './Input';
import ThemeToggle from './ThemeToggle';
import Navbar from './Navbar';

export default function Chat() {
    const [messages, setMessages] = useState([]);
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [selectedAPI, setSelectedAPI] = useState('openai'); // Default to Gemini
    const messagesEndRef = useRef(null);

    const addMessage = (text, isUser) => {
        setMessages((prevMessages) => [...prevMessages, { text, isUser }]);
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        if (isDarkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [isDarkMode]);

    return (
        <div className="h-screen flex flex-col">
            <Navbar selectedAPI={selectedAPI} setSelectedAPI={setSelectedAPI} />
            <div className="flex-1 bg-gray-100 dark:bg-gray-800 p-4 overflow-y-auto relative">
                <div className="fixed top-3 right-4">
                    <ThemeToggle isDarkMode={isDarkMode} setIsDarkMode={setIsDarkMode} />
                </div>
                <div className="max-w-2xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5 }}
                    >
                        {messages.map((message, index) => (
                            <Message key={index} text={message.text} isUser={message.isUser} />
                        ))}
                    </motion.div>
                    <div ref={messagesEndRef} />
                </div>
            </div>
            <div className="bg-white dark:bg-gray-900 p-4">
                <div className="max-w-2xl mx-auto">
                    <Input onSend={addMessage} selectedAPI={selectedAPI} />
                </div>
            </div>
        </div>
    );
}