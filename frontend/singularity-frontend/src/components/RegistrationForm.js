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
      // Convert empty strings to null or remove if the backend expects nullable fields
      // This is a common pattern, adjust based on your GraphQL schema's input type
      const input = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, value === '' ? null : value])
      );

      // Specifically handle required fields that might be empty strings
      // You might want more robust validation here
      if (!input.email || !input.username || !input.password || !input.name || !input.lastName || !input.documentType || !input.documentNumber || !input.documentExpeditionPlace || !input.documentExpeditionDate || !input.country || !input.address || !input.city || !input.phone || !input.celPhone || !input.emergencyName || !input.emergencyPhone) {
           alert('Please fill in all required fields.');
           return;
      }


      const response = await registerUser({
        variables: { input }
      });

      if (response.data.registerUser.success) {
        alert(response.data.registerUser.message);
        // Optionally reset form:
        // setFormData({ ...initialFormDataState }); // Define an initial state object
      } else {
        alert(response.data.registerUser.message);
      }
    } catch (error) {
      alert('Error during registration: ' + error.message);
    }
  };

  const styles = {
    container: {
      maxWidth: '600px', // Reduced from 800px
      margin: '40px auto',
      padding: '40px',
      backgroundColor: 'white',
      borderRadius: '15px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
    title: {
      color: '#003B73',
      fontSize: '2rem',
      marginBottom: '30px',
      fontWeight: 'bold',
      textAlign: 'center', // Added for better centering
    },
    section: {
      marginBottom: '30px',
    },
    sectionTitle: {
      color: '#003B73',
      fontSize: '1.25rem',
      marginBottom: '20px',
      fontWeight: '600',
      borderBottom: '1px solid #E1E1E1', // Added a subtle separator
      paddingBottom: '10px',
    },
    inputContainer: {
      marginBottom: '15px',
    },
    input: {
      width: 'calc(100% - 24px)', // Adjust for padding
      padding: '12px', // Increased padding
      border: '1px solid #E1E1E1',
      borderRadius: '4px',
      fontSize: '1rem', // Increased font size
      backgroundColor: '#FFFFFF',
      transition: 'border-color 0.3s ease, box-shadow 0.3s ease', // Added box-shadow transition
      boxSizing: 'border-box', // Include padding and border in the element's total width and height
    },
     inputFocus: {
      borderColor: '#0077FF',
      boxShadow: '0 0 0 0.2rem rgba(0, 119, 255, 0.25)',
    },
    select: {
      width: '100%',
      padding: '12px', // Increased padding
      border: '1px solid #E1E1E1',
      borderRadius: '4px',
      fontSize: '1rem', // Increased font size
      backgroundColor: '#FFFFFF',
      cursor: 'pointer',
      transition: 'border-color 0.3s ease, box-shadow 0.3s ease', // Added box-shadow transition
      boxSizing: 'border-box', // Include padding and border in the element's total width and height
    },
     selectFocus: {
      borderColor: '#0077FF',
      boxShadow: '0 0 0 0.2rem rgba(0, 119, 255, 0.25)',
    },
    checkboxContainer: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '15px',
    },
    checkbox: {
      marginRight: '8px',
      cursor: 'pointer',
      transform: 'scale(1.2)', // Slightly larger checkbox
    },
    checkboxLabel: {
      color: '#003B73', // Changed color to match titles
      fontSize: '1rem', // Increased font size
      cursor: 'pointer',
    },
    button: {
      width: '100%',
      padding: '12px',
      backgroundColor: '#0077FF',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      fontSize: '1.1rem', // Slightly larger font size
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease, opacity 0.3s ease', // Added opacity transition
      marginTop: '20px', // Added space above the button
    },
    buttonHover: {
      backgroundColor: '#0056b3', // Darker blue on hover
    },
    buttonDisabled: {
        opacity: 0.6,
        cursor: 'not-allowed',
    }
  };

  if (queryLoading) return <p style={{ textAlign: 'center' }}>Loading form data...</p>;
  if (queryError) return <p style={{ textAlign: 'center', color: 'red' }}>Error loading form data: {queryError.message}</p>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>User Registration</h1>

      <form onSubmit={handleSubmit}>
        {/* Basic User Information */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Basic Information</h2>
          <div style={styles.inputContainer}>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="lastName"
              placeholder="Last Name"
              value={formData.lastName || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.checkboxContainer}>
            <input
              type="checkbox"
              name="isMilitar"
              id="militaryStatus"
              checked={formData.isMilitar}
              onChange={handleChange}
              style={styles.checkbox}
            />
            <label
              htmlFor="militaryStatus"
              style={styles.checkboxLabel}
            >
              Military Status
            </label>
          </div>
        </div>

        {/* Document Information */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Document Information</h2>
          <div style={styles.inputContainer}>
            <select
              name="documentType"
              value={formData.documentType || ''}
              onChange={handleChange}
              style={styles.select}
              required
               onFocus={e => e.target.style.borderColor = styles.selectFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.select.border.split(' ')[2]}
            >
              <option value="">Select Document Type</option>
              {queryData?.allDocumentTypes?.map(type => (
                <option key={type.id} value={type.id}>
                  {type.nameTypeDocument}
                </option>
              ))}
            </select>
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="documentNumber"
              placeholder="Document Number"
              value={formData.documentNumber || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="documentExpeditionPlace"
              placeholder="Place of Expedition"
              value={formData.documentExpeditionPlace || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="date"
              name="documentExpeditionDate"
              value={formData.documentExpeditionDate || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
        </div>

        {/* Contact Information */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Contact Information</h2>
          <div style={styles.inputContainer}>
            <select
              name="country"
              value={formData.country || ''}
              onChange={handleChange}
              style={styles.select}
              required
               onFocus={e => e.target.style.borderColor = styles.selectFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.select.border.split(' ')[2]}
            >
              <option value="">Select Country</option>
              {queryData?.allCountries?.map(country => (
                <option key={country.id} value={country.id}>
                  {country.countryName} ({country.countryCode})
                </option>
              ))}
            </select>
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="address"
              placeholder="Address"
              value={formData.address || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="city"
              placeholder="City"
              value={formData.city || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="tel"
              name="phone"
              placeholder="Phone"
              value={formData.phone || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="tel"
              name="celPhone"
              placeholder="Cell Phone"
              value={formData.celPhone || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="text"
              name="emergencyName"
              placeholder="Emergency Contact Name"
              value={formData.emergencyName || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
          <div style={styles.inputContainer}>
            <input
              type="tel"
              name="emergencyPhone"
              placeholder="Emergency Contact Phone"
              value={formData.emergencyPhone || ''}
              onChange={handleChange}
              style={styles.input}
              required
               onFocus={e => e.target.style.borderColor = styles.inputFocus.borderColor}
               onBlur={e => e.target.style.borderColor = styles.input.border.split(' ')[2]}
            />
          </div>
        </div>

        <button
          type="submit"
          style={{
            ...styles.button,
            ...(mutationLoading ? styles.buttonDisabled : {}),
          }}
          disabled={mutationLoading}
          onMouseOver={e => { if (!mutationLoading) e.target.style.backgroundColor = styles.buttonHover.backgroundColor; }}
          onMouseOut={e => { if (!mutationLoading) e.target.style.backgroundColor = styles.button.backgroundColor; }}
        >
          {mutationLoading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
}

export default RegistrationForm;