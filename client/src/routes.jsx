import {
  createHashRouter,
  createRoutesFromElements,
  Route,
  useOutletContext,
  Navigate,
} from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Signup';
import Login from './pages/Login';
// import Layout from './layout/Layout';


const router = createHashRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />}></Route>
      <Route
        path="register"
        element={
          <AuthRoute>
            <Register />
          </AuthRoute>
        }
      ></Route>
      <Route
        path="login"
        element={
          <AuthRoute>
            <Login />
          </AuthRoute>
        }
      ></Route>

      <Route
        path="chat"
        element={
          <PrivateRoute>
            <Chat />
          </PrivateRoute>
        }
      ></Route>

    //</Route>
  )
);

function AuthRoute({ children }) {
  const { user } = useOutletContext();

  return user ? <Navigate to="/" /> : children;
}

function PrivateRoute({ children }) {
  const { user } = useOutletContext();

  return !user ? <Navigate to="/" /> : children;
}
export default router;