import React, {useCallback, useEffect, useState,} from "react";
import { render } from "react-dom";
import Gallery from "react-photo-gallery";
import Carousel, {Modal, ModalGateway} from "react-images";

function App() {
    const [currentImage, setCurrentImage] = useState(0);
    const [viewerIsOpen, setViewerIsOpen] = useState(false);
    const [data, setData] = useState([]);

    const openLightBox = useCallback((event, { photo, index}) => {
        setCurrentImage(index);
        setViewerIsOpen(true);
    }, []);

    const closeLightBox = () => {
        setCurrentImage(0);
        setViewerIsOpen(false);
    };

    useEffect( () => {
        fetch("/gallery/photos/")
            .then(response => response.json())
            .then(data => setData(data));
    }, [])


    return (
    <div>
      <Gallery photos={data} onClick={openLightBox} />
      <ModalGateway>
        {viewerIsOpen ? (
          <Modal onClose={closeLightBox}>
            <Carousel
              currentIndex={currentImage}
              views={data.map(x => ({
                ...x,
                srcset: x.srcSet,
                caption: x.description,
                sizes: x.sizes,
              }))}
            />
          </Modal>
        ) : null}
      </ModalGateway>
    </div>
  );
}
render(<App />, document.getElementById("app"));
