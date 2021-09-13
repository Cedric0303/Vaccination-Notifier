import { useState, useEffect } from "react";
import axios from "axios";

const BASE_URL = process.env.REACT_APP_BACKEND_API_URL

axios.interceptors.request.use(
	(config) => {
		const { origin } = new URL(config.url);
		const allowedOrigins = [BASE_URL];
		console.log(origin)
		console.log(allowedOrigins)
		const token = localStorage.getItem("accessToken"); // get the token
		if (allowedOrigins.includes(origin)) {
			console.log(token);
			config.headers.authorization = `JWT ${token}`; // we put our token in the header
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

// Get the list of users from the database
function getUsers() {
	const endpoint =
		BASE_URL +
		"/api/users";
	return axios
		.get(endpoint, { withCredentials: true })
		.then((res) => res.data);
}

// Use loading, normal, and error states with the returned data
export function useUsers() {
	const [loading, setLoading] = useState(true);
	const [usersData, setUsers] = useState([]);
	const [error, setError] = useState(null);
	useEffect(() => {
		getUsers()
			.then((usersData) => {
				setUsers(usersData);
				setLoading(false);
			})
			.catch((e) => {
				console.log(e);
				setError(e);
				setLoading(false);
			});
	}, []);
	return {
		loading,
		usersData,
		error,
	};
}