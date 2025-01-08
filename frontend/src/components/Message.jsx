import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'; // For GitHub-flavored markdown (optional)

export default function Message({ text, isUser }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
        >
            <div
                className={`max-w-2xl px-4 py-2 rounded-lg break-words whitespace-pre-wrap ${
                    isUser
                        ? 'bg-blue-500 text-white'
                        : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-white'
                }`}
                style={{
                    wordBreak: 'break-word',
                    overflowWrap: 'break-word',
                    whiteSpace: 'pre-wrap',
                }}
            >
                <ReactMarkdown
                    children={text}
                    remarkPlugins={[remarkGfm]} 
                    components={{
                        code({ node, inline, className, children, ...props }) {
                            return inline ? (
                                <code
                                    className={`bg-gray-200 dark:bg-gray-800 text-sm px-1 rounded ${
                                        isUser ? 'text-white' : 'text-gray-800'
                                    }`}
                                    style={{
                                        wordBreak: 'break-word',
                                        overflowWrap: 'break-word',
                                    }}
                                    {...props}
                                >
                                    {children}
                                </code>
                            ) : (
                                <pre
                                    className={`overflow-x-auto p-2 rounded ${
                                        isUser ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-800'
                                    }`}
                                    style={{
                                        whiteSpace: 'pre-wrap', // Ensure wrapping
                                        wordBreak: 'break-word',
                                        overflowWrap: 'break-word',
                                    }}
                                    {...props}
                                >
                                    <code>{children}</code>
                                </pre>
                            );
                        },
                    }}
                />
            </div>
        </motion.div>
    );
}
