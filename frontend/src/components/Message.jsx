import React from 'react';
import { motion } from 'framer-motion';

export default function Message({ text, isUser }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
        >
            <div
                className={`max-w-md p-4 rounded-lg break-words whitespace-pre-wrap ${
                    isUser
                        ? 'bg-blue-500 text-white'
                        : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-white'
                }`}
            >
                {text}
            </div>
        </motion.div>
    );
}

