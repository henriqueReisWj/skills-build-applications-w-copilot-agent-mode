import { useEffect, useMemo, useState } from 'react';

function normalizeRows(data) {
  if (Array.isArray(data)) {
    return data;
  }
  if (Array.isArray(data?.results)) {
    return data.results;
  }
  return [];
}

function getColumnKeys(rows) {
  if (!rows.length) {
    return ['raw'];
  }
  const keySet = new Set();
  rows.forEach((row) => {
    if (row && typeof row === 'object') {
      Object.keys(row).forEach((key) => keySet.add(key));
    }
  });
  return Array.from(keySet);
}

function formatCellValue(value) {
  if (value === null || value === undefined) {
    return '-';
  }
  if (typeof value === 'object') {
    return JSON.stringify(value);
  }
  return String(value);
}

function ApiTableCard({ title, endpointPath }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [showModal, setShowModal] = useState(false);

  const endpoint = process.env.REACT_APP_CODESPACE_NAME
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/${endpointPath}/`
    : `http://localhost:8000/api/${endpointPath}/`;

  useEffect(() => {
    console.log(`${title} endpoint:`, endpoint);

    fetch(endpoint)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log(`${title} fetched data:`, data);
        setItems(normalizeRows(data));
      })
      .catch((err) => {
        setError(err.message || `Failed to load ${title.toLowerCase()}.`);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [endpoint, title]);

  const columns = useMemo(() => getColumnKeys(items), [items]);

  const filteredItems = useMemo(() => {
    if (!query.trim()) {
      return items;
    }
    const normalizedQuery = query.toLowerCase();
    return items.filter((item) => {
      const serialized = JSON.stringify(item).toLowerCase();
      return serialized.includes(normalizedQuery);
    });
  }, [items, query]);

  return (
    <section className="card shadow-sm border-0">
      <div className="card-body">
        <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
          <h2 className="h3 mb-0 text-primary-emphasis">{title}</h2>
          <div className="d-flex gap-2">
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={() => setShowModal(true)}
            >
              Details
            </button>
            <button type="button" className="btn btn-primary" onClick={() => window.location.reload()}>
              Reload Data
            </button>
          </div>
        </div>

        <form className="row g-2 align-items-center mb-3" onSubmit={(event) => event.preventDefault()}>
          <div className="col-sm-8 col-md-6">
            <label htmlFor={`${endpointPath}-search`} className="form-label">
              Search records
            </label>
            <input
              id={`${endpointPath}-search`}
              className="form-control"
              type="text"
              placeholder="Type to filter rows..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </div>
          <div className="col-sm-4 col-md-3">
            <label htmlFor={`${endpointPath}-count`} className="form-label">
              Rows found
            </label>
            <input
              id={`${endpointPath}-count`}
              className="form-control"
              type="text"
              value={String(filteredItems.length)}
              readOnly
            />
          </div>
        </form>

        <p className="mb-3">
          <a href={endpoint} className="link-primary" target="_blank" rel="noreferrer">
            Open API endpoint
          </a>
        </p>

        {loading && <div className="alert alert-info mb-0">Loading data...</div>}
        {!loading && error && <div className="alert alert-danger mb-0">Error: {error}</div>}

        {!loading && !error && (
          <div className="table-responsive">
            <table className="table table-striped table-hover align-middle table-bordered mb-0">
              <thead className="table-light">
                <tr>
                  <th scope="col" style={{ width: '70px' }}>
                    #
                  </th>
                  {columns.map((column) => (
                    <th key={column} scope="col">
                      {column}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filteredItems.length === 0 && (
                  <tr>
                    <td colSpan={columns.length + 1} className="text-center text-muted py-4">
                      No records available.
                    </td>
                  </tr>
                )}
                {filteredItems.map((item, index) => (
                  <tr key={item?.id || item?._id || index}>
                    <th scope="row">{index + 1}</th>
                    {columns.map((column) => (
                      <td key={`${column}-${index}`}>{formatCellValue(item?.[column])}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showModal && (
        <>
          <div className="modal fade show d-block" tabIndex="-1" role="dialog" aria-modal="true">
            <div className="modal-dialog modal-dialog-centered" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h3 className="modal-title h5 mb-0">{title} Summary</h3>
                  <button
                    type="button"
                    className="btn-close"
                    aria-label="Close"
                    onClick={() => setShowModal(false)}
                  />
                </div>
                <div className="modal-body">
                  <p className="mb-1">
                    <strong>Total rows:</strong> {items.length}
                  </p>
                  <p className="mb-1">
                    <strong>Filtered rows:</strong> {filteredItems.length}
                  </p>
                  <p className="mb-0">
                    <strong>Endpoint:</strong> {endpoint}
                  </p>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show" onClick={() => setShowModal(false)} />
        </>
      )}
    </section>
  );
}

export default ApiTableCard;
