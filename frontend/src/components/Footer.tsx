interface FooterProps {
    year : number;
}

const Footer = ({year}: FooterProps )=> {
    return (
        <footer className='text-center py-4 text-gray-500'>
            <p>© {year} TTG Shop - All rights reserved.</p>
        </footer>
    )
}
export default Footer