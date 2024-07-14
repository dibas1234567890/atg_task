import React, { useState, useEffect } from "react";
import axios from "axios";

const BlogForm = () => {

    const token = localStorage.getItem('access_token');


    const [formData, setFormData] = useState({
        title: '',
        image: null,
        category: '',
        summary: '',
        content: '',
        status: ''
    });
    const [error, setError] = useState('');
    const [categories, setCategories] = useState([]);
    const [statuses, setStatuses] = useState([
        { value: 'draft', label: 'Draft' },
        { value: 'published', label: 'Published' },
    ]);


    const getCsrfToken = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/csrf_token', {
                withCredentials: true
            });
            return response.data.csrfToken;
        } catch (error) {
            console.error('Error fetching CSRF token:', error);
            setError('Error fetching CSRF token');
            return null;
        }
    };

    useEffect(  () => {

        const csrfToken =  getCsrfToken();
        const fetchCategories = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/categories', 
                    {headers: {
                        'X-CSRFToken': csrfToken,
                                   'Authorization': `Bearer ${token}`
                     }}  );
                setCategories(response.data); 
            } catch (error) {
                setError('Failed to fetch categories');
            }
        };
        fetchCategories();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleFileChange = (e) => {
        setFormData({
            ...formData,
            image: e.target.files[0],
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formDataToSubmit = new FormData();
        Object.keys(formData).forEach((key) => {
            formDataToSubmit.append(key, formData[key]);
        });

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/blogs/', formDataToSubmit, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log("Blog created:", response.data);
        } catch (error) {
            setError(error.response.data.detail || 'An error occurred');
        }
    };

    return (
        <div className="container">
            <h2>Create Blog</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title</label>
                    <input
                        id="title"
                        type="text"
                        className="form-control"
                        value={formData.title}
                        name="title"
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="image">Image</label>
                    <input
                        id="image"
                        type="file"
                        className="form-control"
                        name="image"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="category">Category</label>
                    <select
                        id="category"
                        className="form-control"
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select Category</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.category_name}
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="summary">Summary   </label>
                    <input
                        id="summary"
                        type="text"
                        className="form-control"
                        value={formData.summary}
                        name="summary"
                        onChange={handleChange}
                        placeholder="Will be truncated in the frontend, doctor will be allowed to add more than 15"
                        required
                    />
                </div>
                <div>
                    <label htmlFor="content">Content</label>
                    <textarea rows="4" cols="50"
                        id="content"
                        className="form-control"
                        value={formData.content}
                        name="content"
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="status">Status</label>
                    <select
                        id="status"
                        className="form-control"
                        name="status"
                        value={formData.status}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select Status</option>
                        {statuses.map((status) => (
                            <option key={status.value} value={status.value}>
                                {status.label}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="mt-2">
                    <button type="submit" className="btn btn-primary">Create Blog</button>
                </div>
            </form>
        </div>
    );
};

export default BlogForm;
