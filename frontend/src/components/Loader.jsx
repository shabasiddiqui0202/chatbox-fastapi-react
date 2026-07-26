function Loader({ text = "Loading..." }) {
  return (
    <div className="loader">
      <div className="spinner"></div>

      <p>{text}</p>
    </div>
  );
}
export default Loader;
