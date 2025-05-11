import React, { useState } from 'react';
import { useMutation, useQuery, gql } from '@apollo/client';

const GET_INITIAL_DATA = gql`
  query {
    allCountries {
      id
      countryCode
      countryName
    }
    allDocumentTypes {
      id
      nameTypeDocument
    }
  }
`;

const REGISTER_USER = gql`
  mutation RegisterUser($input: UserRegistrationInput!) {
    registerUser(input: $input) {
      success
      message
      user {
        id
        email
      }
    }
  }
`;

function RegistrationForm() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    lastName: '',
    name: '',
    isMilitar: false,
    documentType: '',
    documentNumber: '',
    documentExpeditionPlace: '',
    documentExpeditionDate: '',
    country: '',
    address: '',
    city: '',
    phone: '',
    celPhone: '',
    emergencyName: '',
    emergencyPhone: ''
  });

  const { loading: queryLoading, error: queryError, data: queryData } = useQuery(GET_INITIAL_DATA);
  const [registerUser, { loading: mutationLoading }] = useMutation(REGISTER_USER);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const input = {
        email: formData.email,
        username: formData.username,
        password: formData.password,
        lastName: formData.lastName,
        name: formData.name,
        isMilitar: formData.isMilitar,
        documentType: formData.documentType,
        documentNumber: formData.documentNumber,
        documentExpeditionPlace: formData.documentExpeditionPlace,
        documentExpeditionDate: formData.documentExpeditionDate,
        country: formData.country,
        address: formData.address,
        city: formData.city,
        phone: formData.phone,
        celPhone: formData.celPhone,
        emergencyName: formData.emergencyName,
        emergencyPhone: formData.emergencyPhone
      };

      const response = await registerUser({
        variables: { input }
      });

      if (response.data.registerUser.success) {
        alert(response.data.registerUser.message);
        // Reset form or redirect
      } else {
        alert(response.data.registerUser.message);
      }
    } catch (error) {
      alert('Error during registration: ' + error.message);
    }
  };

  if (queryLoading) return <p>Loading...</p>;
  if (queryError) return <p>Error loading form data: {queryError.message}</p>;

  const formStyle = {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px'
  };

  const inputStyle = {
    width: '100%',
    padding: '8px',
    marginBottom: '10px',
    border: '1px solid #ccc',
    borderRadius: '4px'
  };

  const buttonStyle = {
    width: '100%',
    padding: '10px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h2>User Registration</h2>
      
      {/* Basic User Information */}
      <h3>Basic Information</h3>
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={formData.name}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="lastName"
        placeholder="Last Name"
        value={formData.lastName}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <label style={{ display: 'block', marginBottom: '10px' }}>
        <input
          type="checkbox"
          name="isMilitar"
          checked={formData.isMilitar}
          onChange={handleChange}
        />
        {' '}Military Status
      </label>

      {/* Document Information */}
      <h3>Document Information</h3>
      <select
        name="documentType"
        value={formData.documentType}
        onChange={handleChange}
        style={inputStyle}
        required
      >
        <option value="">Select Document Type</option>
        {queryData?.allDocumentTypes?.map(type => (
          <option key={type.id} value={type.id}>
            {type.nameTypeDocument}
          </option>
        ))}
      </select>
      <input
        type="text"
        name="documentNumber"
        placeholder="Document Number"
        value={formData.documentNumber}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="documentExpeditionPlace"
        placeholder="Place of Expedition"
        value={formData.documentExpeditionPlace}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="date"
        name="documentExpeditionDate"
        value={formData.documentExpeditionDate}
        onChange={handleChange}
        style={inputStyle}
        required
      />

      {/* Contact Information */}
      <h3>Contact Information</h3>
      <select
        name="country"
        value={formData.country}
        onChange={handleChange}
        style={inputStyle}
        required
      >
        <option value="">Select Country</option>
        {queryData?.allCountries?.map(country => (
          <option key={country.id} value={country.id}>
            {country.countryName} ({country.countryCode})
          </option>
        ))}
      </select>
      <input
        type="text"
        name="address"
        placeholder="Address"
        value={formData.address}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="city"
        placeholder="City"
        value={formData.city}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="tel"
        name="phone"
        placeholder="Phone"
        value={formData.phone}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="tel"
        name="celPhone"
        placeholder="Cell Phone"
        value={formData.celPhone}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="text"
        name="emergencyName"
        placeholder="Emergency Contact Name"
        value={formData.emergencyName}
        onChange={handleChange}
        style={inputStyle}
        required
      />
      <input
        type="tel"
        name="emergencyPhone"
        placeholder="Emergency Contact Phone"
        value={formData.emergencyPhone}
        onChange={handleChange}
        style={inputStyle}
        required
      />

      <button 
        type="submit" 
        style={buttonStyle}
        disabled={mutationLoading}
      >
        {mutationLoading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}

export default RegistrationForm;