<template>
    <div
        class="container-fluid no-gutter big-div"
        :style="cropBoxCssVars"
    >
        <!-- <div
            v-show="imagePreviewFile == null"
            id="divCrop"
            style="display: none"
            :style="cropBoxCssVars"
            @click="toChooseImages()"
        ></div> -->
        <div class="row" @mousemove="setCoradinatesForCropBox">
            <div class="col-md-12 title">
                <h1>Put your nt-image here and we measure it for you!</h1>
            </div>
            <div class="col-md-12 box-push-image">
                <input
                    type="file"
                    name="image"
                    id="ntimage"
                    ref="putYourImage"
                    @change="getPreview"
                >
                <div class="image__show" @click="toChooseImages">
                    <img v-show="imagePreviewFile != null" :src="imagePreviewFile" alt="NT IMAGE">
                </div>
            </div>
            <div class="col-md-12 control-upload">
                <button class="btn btn-primary" @click="toUploadImage" :disabled="imagePreviewFile == null" >Upload</button>
                <button class="btn btn-primary" @click="toChooseAnotherImages" :disabled="imagePreviewFile == null" >Upload new</button>
                    <!-- v-show="imagePreviewFile != null" -->
            </div>

            <div v-show="imagePreviewFile != null"  class="col-md-9 box-mask-predict">
                <h1>Mask predict</h1>
            </div>
            <div v-show="imagePreviewFile != null" class="col-md-3 box-nt-measure">
                <h1>NT result</h1>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
// axios.defaults.withCredentials = true;

export default {
    data () {
        return {
            imagePreviewFile: null,
            imageFileUpload: null,
            csrf: null,
            coradinateCropBox: {
                x: 0,
                y: 0,
            },
            delimiters: ['[[', ']]'],
        }
    },
    watch: {
        imagePreviewFile() {
            // console.log(this.imagePreviewFile);
            document.getElementById('ntimage').removeAttribute('ref');
        },
        'coradinateCropBox.x'() {
            // console.log(screen.height);
            // console.log(screen.width);
        }
    },
    computed: {
        cropBoxCssVars() {
            return {
                '--top': this.coradinateCropBox.y > screen.height ? 0 + 'px' : this.coradinateCropBox.y + 'px',
                '--left': this.coradinateCropBox.x > screen.width ? 0 + 'px' : this.coradinateCropBox.x + 'px',
                '--imageUrl': this.imagePreviewFile,
            }
        }
    },
    methods: {
        async getToken() {
            if (this.csrf == null) {
                var response = await axios.get("http://127.0.0.1:8000/ntdemo/csrf");
                if (response.status == 200) {
                    this.csrf = response.data.csrf_token;
                    return response.data;
                } else {
                    return false;
                }
            }
            return this.csrf;
        },

        toChooseImages(e) {
            if (this.imagePreviewFile == null) {
                e.target.value = null;
                this.$refs.putYourImage.click();
            }
        },

        toChooseAnotherImages(e) {
            this.imagePreviewFile = null;
            e.target.value = null;
            this.$refs.putYourImage.click();
        },

        async toUploadImage() {
            // const data = await this.getToken();

            // console.log('token: ', data.csrf_token);

            console.log('its working');
            let dataForm = new FormData();
            dataForm.append('images', this.imageFileUpload);
            dataForm.append('cropCorradinate', this.coradinateCropBox);

            var response = await axios.post('http://127.0.0.1:8000/ntdemo/upload', dataForm, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": "{{ csrf_token }}",
                }
            }).then(() => { console.log('success'); })
              .catch(() => { console.log('failed'); })

            return response;
        },

        getPreview(e) {
            var file = e.target.files;
            this.imageFileUpload = file[0];
            this.imagePreviewFile = URL.createObjectURL(file[0])
        },

        setCoradinatesForCropBox(e) {
            this.coradinateCropBox.x = e.clientX;
            this.coradinateCropBox.y = e.clientY;
        },
    }
}
</script>

<style scope>
    * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
    }

    .big-div {
        position: relative;
    }

    #divCrop {
        position: absolute;
        height: 256px;
        width: 256px;
        background-color: rgba(0, 0, 0, 0.4);
        border: 2px dashed #000;
        /* top: 1920px;
        left: 1080px; */
        top: var(--top);
        left: var(--left);
        /* transition: 0.25s; */
        z-index: 100;
    }

    .title {
        text-align: center;
    }

    .title > h1 {
        word-wrap: break-word;
    }

    .box-push-image {
        text-align: center;
        background-color: rgb(114, 30, 30);
    }

    #ntimage {
        display: none;
    }

    .image__show {
        overflow: auto;
        height: 60vh;
        width: 100%;
        /* display: flex; */
        /* justify-content: center; */
        /* justify-items: center; */
    }

    .image__show > img {
        object-fit: contain;
    }

    .control-upload {
        background-color: rgb(213, 202, 223);
        padding: 10px 0;
        display: flex;
        justify-content: start;
        align-items: center;
    }

    .control-upload button {
        margin: 0 10px;
    }

    .box-mask-predict {
        text-align: center;
        background-color: aquamarine;
    }

    .box-nt-measure {
        text-align: center;
        background-color: blue;
    }
</style>
