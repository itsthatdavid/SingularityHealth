import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import RegistrationForm from './components/RegistrationForm';

const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql/',
  cache: new InMemoryCache(),
  credentials: 'include',
});

function App() {
  return (
    <ApolloProvider client={client}>
      <div className="App">
        <RegistrationForm />
      </div>
    </ApolloProvider>
  );
}

export default App;