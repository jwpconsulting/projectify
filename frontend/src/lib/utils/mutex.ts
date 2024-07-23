// SPDX-License-Identifier: MIT
/*
 * MIT License
 *
 * Copyright (c) 2023 Dmitrii Baranov
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
// eslint-disable-next-line @typescript-eslint/no-empty-function
function releaseStub() {}

export class Mutex {
    private m_lastPromise: Promise<void> = Promise.resolve();

    /**
     * Acquire lock
     * @param [bypass=false] option to skip lock acquisition
     */
    public async obtain(bypass = false): Promise<() => void> {
        let release = releaseStub;
        if (bypass) return release;
        const lastPromise = this.m_lastPromise;
        this.m_lastPromise = new Promise<void>(
            (resolve) => (release = resolve),
        );
        await lastPromise;
        return release;
    }
}
