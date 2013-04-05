Unofficial Magyar Posta Tracker API with Requests
=================================================

API usage
---------

Two methods make functionality available, they both take a single parameter called `number`, which is the document number of the package to be tracked. They only differ in that `track_item_iter` is a generator that yields `TrackEntry` named tuples, while `track_item` returns a list of such objects.

CLI usage
---------

The tracking number should be supplied as a command line parameter. Usage example:

	$ python mptr.py RT123456789HK
	2013-03-26T16:54:00     (HONG KONG)     Küldemény információ:Küldemény felvéve / Item accepted

Disclaimer
----------

This tool was created as a proof of concept and should not be used on the real http://posta.hu/ page without prior consent. As the MIT license states:

	IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
	CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
	TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

License
-------

The whole project is available under MIT license.

Dependencies
------------

 - Python 2.x (at least 2.6, tested on 2.7.3)
 - Requests (Debian/Ubuntu package: `python-requests`)
 - LXML (Debian/Ubuntu package: `python-lxml`)
