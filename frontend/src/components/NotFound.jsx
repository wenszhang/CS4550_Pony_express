import React from 'react';

export default class NotFound extends React.Component {
    render() {
        return (
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
                <h1>404 Not Found</h1>
                <p>The page you are looking for does not exist or another error occurred.</p>
                <p><a href="/">Go back to the homepage</a></p>
            </div>
        );
    }
}
