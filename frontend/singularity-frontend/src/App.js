import { ApolloClient, InMemoryCache, ApolloProvider, createHttpLink } from '@apollo/client';
import RegistrationForm from './components/RegistrationForm';

const httpLink = createHttpLink({
  uri: 'http://localhost:8000/graphql/',
  credentials: 'same-origin',
  headers: {
    'Content-Type': 'application/json',
  },
});

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache()
});

function App() {
  const styles = {
    app: {
      minHeight: '100vh',
      backgroundColor: '#F0F9FF', // Light blue background
      padding: '20px',
    },
    header: {
      maxWidth: '800px',
      margin: '0 auto 20px',
      display: 'flex',
      alignItems: 'center',
    },
    logo: {
      fontSize: '24px',
      color: '#003B73',
      fontWeight: 'bold',
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
    },
    logoIcon: {
      color: '#0077FF',
    },
  };

  return (
    <ApolloProvider client={client}>
      <div style={styles.app}>
        <header style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>★</span>
            Singularity Health
          </div>
        </header>
        <RegistrationForm />
      </div>
    </ApolloProvider>
  );
}

export default App;