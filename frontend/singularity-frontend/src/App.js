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
      // Replaced backgroundColor with backgroundImage for a gradient
      backgroundImage: 'linear-gradient(to bottom right, #F0F9FF, #CFEEFF)', // Subtle blue gradient
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
     logoImage: { // Added style for the image
        height: '40px', // Example size, adjust as needed
        marginRight: '10px',
    }
  };

  return (
    <ApolloProvider client={client}>
      <div style={styles.app}>
        <header style={styles.header}>
          <div style={styles.logo}>
              <img
                src="/logo192.png"
                alt="Singularity Health Logo"
                style={styles.logoImage} // Apply the image style
              />
              Singularity Health
            </div>
        </header>
        <RegistrationForm />
      </div>
    </ApolloProvider>
  );
}

export default App;