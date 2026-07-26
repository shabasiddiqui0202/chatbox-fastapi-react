export const createSocket = (username) => {
  return new WebSocket(`ws://localhost:8001/ws/${username}`);
};
